#pragma once
#include <string>

class Time
{
public:
    Time(int h = INT_MAX, int m = INT_MAX) : hours(h), minutes(m) {}

    Time operator +(Time t2)
    {
        Time result(hours, minutes);
        result.minutes = minutes + t2.minutes;
        result.hours = hours + t2.hours;
        bool over = (result.minutes - 60 >= 0);
        if (over)
        {
            result.hours += 1;
            result.minutes -= 60;
        }
        return result;
    }

    bool operator <(const Time& t2) const
    {
        if (hours < t2.hours || (hours == t2.hours && minutes < t2.minutes))
            return true;
        return false;
    }

    bool operator >(const Time& t2) const
    {
        if (hours > t2.hours || (hours == t2.hours && minutes > t2.minutes))
            return true;
        return false;
    }

    bool operator ==(const Time& t2) const
    {
        if (hours == t2.hours && minutes == t2.minutes)
            return true;
        return false;
    }

    bool operator >=(const Time& t2) const
    {
        if ((*this) == t2 || (*this) > t2)
            return true;
        return false;
    }


    std::string toString(bool onlyMinutes = false) const
    {
        std::string m = std::to_string(minutes);
        if (minutes < 10)
            m = "0" + m;
        if (onlyMinutes)
            return m;
        return std::to_string(hours) + ":" + m;
    }

    int hours;
    int minutes;
};