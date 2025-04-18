from pathlib import Path

from typer.testing import CliRunner

runner = CliRunner()

TEST_DATA_DIR = Path(__file__).parent / "test_data"


def test_gmock():
    pass


# def test_gmock_single_file(tmp_path):
#     """测试单个头文件生成mock"""
#     header = TEST_DATA_DIR / "BasicInterface.h"
#     mock_output = tmp_path / "BasicInterface_mock.h"
#     result = runner.invoke(app, [
#         "autogtest",
#         str(header),
#         "--mock", str(mock_output),
#         "--include", str(TEST_DATA_DIR)
#     ])

#     assert result.exit_code == 0
#     assert mock_output.exists()

#     content = mock_output.read_text()
#     assert "class BasicInterfaceMock" in content
#     assert "MOCK_METHOD(void, DoSomething, (int param), (override));" in content

# def test_gmock_batch_processing(tmp_path):
#     """测试批量生成mock文件"""
#     input_dir = Path("tests/test_data")
#     output_dir = tmp_path / "mocks"

#     result = runner.invoke(app, [
#         "autogtest",
#         str(input_dir),
#         "--mock", str(output_dir),
#         "--include", "tests/test_data"
#     ])

#     assert result.exit_code == 0
#     assert (output_dir / "BasicInterface_mock.h").exists()
#     assert (output_dir / "NestedNamespace_mock.h").exists()

# def test_gmock_method_signatures(tmp_path):
#     """验证复杂方法签名生成"""
#     header = Path("tests/test_data/AdvancedInterface.h")
#     mock_output = tmp_path / "AdvancedInterface_mock.h"

#     runner.invoke(app, [
#         "autogtest",
#         str(header),
#         "--mock", str(mock_output),
#         "--include", "tests/test_data"
#     ])

#     content = mock_output.read_text()
#     # 验证const方法
#     assert re.search(r'MOCK_METHOD\(int,\s+GetValue,\s\(\),\s\(const,\soverride\)\);', content)
#     # 验证noexcept
#     assert re.search(r'MOCK_METHOD\(void,\s+CriticalOperation,\s\(\),\s\(noexcept,\soverride\)\);', content)
#     # 验证参数类型
#     assert "MOCK_METHOD(std::string, Process, (const std::string& input), (override));" in content

# def test_gmock_namespace_handling(tmp_path):
#     """测试命名空间处理"""
#     header = Path("tests/test_data/NestedNamespace.h")
#     mock_output = tmp_path / "NestedNamespace_mock.h"

#     runner.invoke(app, [
#         "autogtest",
#         str(header),
#         "--mock", str(mock_output),
#         "--include", "tests/test_data"
#     ])

#     content = mock_output.read_text()
#     assert "namespace outer::inner" in content
#     assert "class DataServiceMock" in content
