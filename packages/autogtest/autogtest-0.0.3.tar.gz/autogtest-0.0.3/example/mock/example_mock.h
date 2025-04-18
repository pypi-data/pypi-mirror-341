/**
 * generate by [autogmock](https://github.com/10-neon/autogtest)
 */
#pragma once
#include <gmock/gmock.h>
#include "example/impl/example.h"

namespace example {

class XXXMock: public IXXX {
public:

    MOCK_METHOD(CCC, doSomething, (const DDD& ddd), (override));

    MOCK_METHOD(void, another, (), (override const));

};

class IXXX::TracerMock: public IXXX::ITracer {
public:

    MOCK_METHOD(void, onZZZ, (const IAAA& aaa), (override));

};

} // namespace example

namespace example::A {

class ZZZMock: public ZZZ {
public:

    MOCK_METHOD(void, xxx, (), (override const noexcept &&));

};

} // namespace example::A
