#pragma once
#include <memory>
#include <list>
#include "example/xxx.h"

namespace example {

class IXXX : public IYYY {
public:
    class ITracer {
    public:
        virtual ~ITracer() = default;
        virtual void onZZZ(IAAA const& aaa) = 0;
    };
    using CCC = IBBB::CCC;

    virtual ~IXXX() = default;
    virtual CCC doSomething(DDD const& ddd) = 0;
    virtual void another() const = 0;
};

namespace A {
using IZZZ = IXXX;
class XXX : public IZZZ {
public:
    XXX(std::shared_ptr<UUU> state, std::shared_ptr<ITracer> tracer);
    ~XXX() override = default;
    CCC doSomething(DDD const& ddd) override;
    void another() const override;

protected:
    std::shared_ptr<DDD> ddd_;
    std::shared_ptr<ITracer> tracer_;
    std::list<notnull<std::unique_ptr<DDD>>> ddd_list_;
};

class ZZZ {
    virtual void xxx() && const noexcept  = 0;
};
}

}  // namespace example
