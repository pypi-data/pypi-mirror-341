import os
from typing import Annotated, Optional

import typer
from cxxheaderparser.simple import ClassScope, NamespaceScope, ParsedData, parse_file
from cxxheaderparser.types import Method
from jinja2 import BaseLoader, Environment, FileSystemLoader, Template

jinja2_default_template = """/**
 * generate by [autogmock](https://github.com/10-neon/autogtest)
 */
#pragma once
#include <gmock/gmock.h>
#include "{{ header }}"
{% for namespace, items in gmock_data | groupby('namespace') %}
namespace {{ namespace }} {
{% for item in items %}
class {{ item.name }}: public {{ item.interface }} {
public:
    {% for method in item.methods | sort %}
    {{ method }}
    {% endfor %}
};
{% endfor %}
} // namespace {{ namespace }}
{% endfor %}
"""


class GMockMethod:
    def __init__(self, name: str) -> None:
        self.name = name
        self.qualifier: list[str] = ["override"]
        self.params: list[str] = []
        self.ret: str = ""

    def format(self) -> str:
        params_str = ", ".join(self.params)
        qualifier_str = " ".join(self.qualifier)
        return f"MOCK_METHOD({self.ret}, {self.name}, ({params_str}), ({qualifier_str}));"


class GMockClassModel:
    def __init__(self, classname: str, namespace: str) -> None:
        self.classname: str = classname
        self.parent_class: Optional[GMockClassModel] = None
        self.namespace: str = namespace
        self.mock_methods: list[GMockMethod] = []

    def getClassname(self) -> str:
        if self.parent_class:
            return self.parent_class.getClassname() + "::" + self.classname
        return self.classname

    def getMockClassname(self) -> str:
        mock_classname_parts: list[str] = self.getClassname().split("::")
        mock_classname_parts[-1] = mock_classname_parts[-1].removeprefix("I")
        mock_classname_parts[-1] = mock_classname_parts[-1].removesuffix("Interface")
        mock_classname: str = "::".join(mock_classname_parts)
        mock_classname += "Mock"
        return mock_classname

    def tryAddGMockMethod(self, method_scope: Method) -> bool:
        if not method_scope.pure_virtual:
            return False
        mock_method = GMockMethod(method_scope.name.format())
        for param in method_scope.parameters:
            mock_method.params.append(param.format())
        if method_scope.return_type is None:
            mock_method.ret = "void"
        else:
            mock_method.ret = method_scope.return_type.format()
        if method_scope.const:
            mock_method.qualifier.append("const")
        if method_scope.constexpr:
            mock_method.qualifier.append("constexpr")
        if method_scope.noexcept:
            mock_method.qualifier.append("noexcept")
        if method_scope.ref_qualifier:
            mock_method.qualifier.append("&&")
        self.mock_methods.append(mock_method)
        return True

    def json(self) -> dict:
        return {
            "namespace": self.namespace,
            "name": self.getMockClassname(),
            "interface": self.getClassname(),
            "methods": [method.format() for method in self.mock_methods],
        }

    def format(self) -> str:
        methods_section = "\n    ".join([method.format() for method in self.mock_methods])
        return f"""namespace {self.namespace} {{

class {self.getMockClassname()}Mock: public {self.getClassname()} {{
public:
    {methods_section}
}};

}} // namespace {self.namespace}
"""


class MockGenerator:
    def __init__(self, data: ParsedData) -> None:
        self.data: ParsedData = data
        self.namespace: list[str] = []
        self.classes: list[GMockClassModel] = []

    def parse(self) -> None:
        self.visitNamespaceScope(self.data.namespace)

    def visitNamespaceScope(self, namespace_scope: NamespaceScope) -> None:
        self.namespace.append(namespace_scope.name)
        for class_scope in namespace_scope.classes:
            self.visitClassScope(class_scope=class_scope, parent_class=None)

        for _child_namespace_name, child_namespace_scope in namespace_scope.namespaces.items():
            self.visitNamespaceScope(namespace_scope=child_namespace_scope)
        self.namespace.pop()

    def visitClassScope(self, class_scope: ClassScope, parent_class: Optional[GMockClassModel]) -> None:
        mock_class = self.tryAddMockClassModel(class_scope=class_scope, parent_class=parent_class)
        for child_class_scope in class_scope.classes:
            self.visitClassScope(class_scope=child_class_scope, parent_class=mock_class)

    def isTargetClass(self, class_scope: ClassScope) -> bool:
        return any(method.pure_virtual for method in class_scope.methods)

    def tryAddMockClassModel(
        self, class_scope: ClassScope, parent_class: Optional[GMockClassModel] = None
    ) -> GMockClassModel:
        mock_class = GMockClassModel(
            classname=self.classname(class_scope=class_scope), namespace=self.currentNamespace()
        )
        mock_class.parent_class = parent_class
        [mock_class.tryAddGMockMethod(method) for method in class_scope.methods]
        if self.isTargetClass(class_scope=class_scope):
            self.classes.append(mock_class)
        return mock_class

    def classname(self, class_scope: ClassScope) -> str:
        return class_scope.class_decl.typename.format().replace("class ", "").replace("struct ", "")

    def currentNamespace(self) -> str:
        return "::".join(self.namespace).removeprefix("::")


def write_file_if_not_exist(filepath: str, content: str) -> None:
    directory = os.path.dirname(filepath)
    if not os.path.exists(directory):
        os.makedirs(directory)
    if not os.path.exists(filepath):
        with open(filepath, "w") as file:
            file.write(content)


def create_gmock_file(header: str, output: str, include: str, template: Template) -> bool:
    if not header.endswith(".h") and not header.endswith(".hpp"):
        return False
    generator = MockGenerator(data=parse_file(filename=header))
    generator.parse()
    if len(generator.classes) == 0:
        return False
    json_mock_classes = [mock_class.json() for mock_class in generator.classes]

    context = template.render({"gmock_data": json_mock_classes, "header": os.path.relpath(header, include)})
    write_file_if_not_exist(filepath=output, content=context)
    return True


def create_gmock_files_batch(header_dir: str, mock_dir: str, include: str, template: Template) -> None:
    for root, _, files in os.walk(header_dir):
        for file in files:
            if file.endswith(".h") or file.endswith(".hpp"):
                header = os.path.join(root, file)
                header_relative_path = os.path.relpath(header, header_dir)
                mock_relative_path = header_relative_path.replace(".h", "_mock.h").replace(".hpp", "_mock.hpp")
                mock = os.path.join(mock_dir, mock_relative_path)
                create_gmock_file(header=header, output=mock, include=include, template=template)


app = typer.Typer()


@app.command()
def gmock(
    header: Annotated[str, typer.Argument(help="包含C++头文件的目录或者C++头文件")],
    mock: Annotated[str, typer.Option(help="输出的mock文件存储路径或mock文件路径")],
    include: Annotated[str, typer.Option(help="include base目录")],
    template: Annotated[Optional[str], typer.Option(help="使用的 gmock jinja2模板路径")] = None,
) -> None:
    header = os.path.abspath(header)
    mock = os.path.abspath(mock)
    include = os.path.abspath(include)

    print(
        f"auto gmock, header: {header}, mock: {mock}, template: {template if template else 'None'}, include: {include}"
    )
    if template:
        template = os.path.abspath(template)
        env = Environment(loader=FileSystemLoader(os.path.dirname(template)), autoescape=True)
        jinja2_template: Template = env.get_template(os.path.basename(template))
    else:
        env = Environment(loader=BaseLoader(), autoescape=True)
        jinja2_template = env.from_string(jinja2_default_template)

    if os.path.isdir(header):
        create_gmock_files_batch(header_dir=header, mock_dir=mock, include=include, template=jinja2_template)
    else:
        create_gmock_file(header=header, output=mock, include=include, template=jinja2_template)


def main() -> None:
    app()


if __name__ == "__main__":
    gmock(header="example/impl", mock="example/mock", include="example")
