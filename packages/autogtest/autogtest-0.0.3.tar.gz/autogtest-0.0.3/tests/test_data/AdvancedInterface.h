#pragma once
#include <string>

class AdvancedInterface {
public:
    virtual int GetValue() const = 0;
    virtual void CriticalOperation() noexcept = 0;
    virtual std::string Process(const std::string& input) = 0;
};
