#include "Data.hpp"
#include <algorithm>

void Data::addTram(std::string filename)
{
    // instanitates tram struct before adding it to data class
    std::ifstream is(filename);
    if (!is.good())
    {
        throw std::runtime_error("Cannot open file");
    }
    Tram t;
    std::string line;
    std::getline(is, line);             // line contains only the tram number
    int tramNumber = std::stoi(line);
    std::getline(is, line);             // contains one of the starting tram stops
    t.startA = line;
    std::getline(is, line);             // contains only the other stop from which the tram starts at
    t.startB = line;
    std::getline(is, line);             // blank line

    std::getline(is, line);             // first of the lines in the form (X);(TIME_FROM_START_A_TO_X);(.._START_B_TO_X)

    std::string maxStop = "";
    // adds travel times to each stop from both directions
    while (line.size() > 0)
    {
        auto tokens = getTokens(line, ';');
        std::string stop = tokens[0];
        std::string tA = tokens[1]; std::string tB = tokens[2];
        int timeA;
        int timeB;
        if (tA == "x")
            timeA = INT_MAX;
        else
            timeA = std::stoi(tA);
        if (tB == "x")
            timeB = INT_MAX;
        else
            timeB = std::stoi(tB);

        t.stops.push_back(stop);
        t.timesA.insert_or_assign(stop, timeA);
        t.timesB.insert_or_assign(stop, timeB);

        // keep track of stop with longest name for easier formatting of tram stop column in outputs
        if (stop.size() > maxStop.size())
            maxStop = stop;

        if (stops.find(stop) == stops.end())
        {
            std::list<int> newList;
            stops.insert_or_assign(stop, newList);
        }
        stops[stop].push_back(tramNumber);

        std::getline(is, line);        // read next line
    }

    stopColumn = maxStop.size();

    // each of the following lines contains all departure times from a starting stop, where each day_type has one line
    // first three lines are departures from startA
    std::getline(is, line);
    auto times = get_times(line);
    t.departuresA.insert_or_assign(workday, times);
    std::getline(is, line);
    times = get_times(line);
    t.departuresA.insert_or_assign(saturday, times);
    std::getline(is, line);
    times = get_times(line);
    t.departuresA.insert_or_assign(sunday, times);

    std::getline(is, line);     // blank line to seperate startA and startB

    // departures from startB
    std::getline(is, line);
    times = get_times(line);
    t.departuresB.insert_or_assign(workday, times);
    std::getline(is, line);
    times = get_times(line);
    t.departuresB.insert_or_assign(saturday, times);
    std::getline(is, line);
    times = get_times(line);
    t.departuresB.insert_or_assign(sunday, times);
    trams.insert_or_assign(tramNumber, t);
}

std::string Data::tram_full_timetable(int tramNum, day_type day)
{
    std::string result = "tram " + std::to_string(tramNum) + ", " + daytypeToString(day) + "\n";
    size_t i = 0;
    Tram& tram = trams.at(tramNum);
    result += "Direction: " + tram.startB + " \n";
    // iterate through all departures from start A
    while (i < tram.departuresA[day].size())
    {
        // 10 departures per line
        int cap;
        if (i + 10 < tram.departuresA[day].size())
            cap = i + 10;
        else
        {
            cap = tram.departuresA[day].size();
        }
        // fill next 10 departures for each stop
        for (std::string stop : tram.stops)
        {
            std::string line = stop;
            line += fillFirstCol(line);
            size_t j = i;
            while (j < cap)
            {
                Time nextTime = tram.departuresA.at(day)[j] + Time(0, tram.timesA[stop]);
                line += nextTime.toString() + "\t";
                j++;
            }
            if (tram.timesA[stop] != INT_MAX)
                result += line + "\n";
        }
        result += " \n";
        i = cap;
    }

    i = 0;
    // stops reversed to represent route from startB to startA
    // approach is same as above except this time for startB
    auto revStops = tram.stops;
    std::reverse(revStops.begin(), revStops.end());
    while (i < tram.departuresB[day].size())
    {
        int cap;
        if (i + 10 < tram.departuresB[day].size())
            cap = i + 10;
        else
        {
            cap = tram.departuresB[day].size();
        }
        for (std::string stop : revStops)
        {
            std::string line = stop;
            line += fillFirstCol(line);
            size_t j = i;
            while (j < cap)
            {
                Time nextTime = tram.departuresB.at(day)[j] + Time(0, tram.timesB[stop]);
                line += nextTime.toString() + "\t";
                j++;
            }
            if (tram.timesB[stop] != INT_MAX)
                result += line + " \n";
        }
        result += " \n";
        i = cap;
    }

    return result;
}

std::string Data::tram_stop_timetable(int tramNum, std::string stopName, day_type day)
{
    int hour;
    size_t i = 0;
    Tram& tram = trams.at(tramNum);
    if (tram.timesA.find(stopName) == tram.timesA.end())        //invalid input
        return "Tram " + std::to_string(tramNum) + " does not stop at " + stopName;
    std::string result = "Tram: " + std::to_string(tramNum) +
        ", Stop: " + stopName +
        ", " + daytypeToString(day) + " \n";
    int timeToStop = tram.timesA[stopName];

    if (timeToStop != INT_MAX)      // time == INT_MAX means that the tram doesn't stop at this stop going in direction A->B
    {
        result += "Direction: " + tram.startB + " \n";
        result += "Hour\tMinute\t \n";
    }
    hour = (tram.departuresA[day][0] + Time(0, timeToStop)).hours;
    std::string line = std::to_string(hour) + "\t";
    // iterate through all departures from start A
    while (timeToStop != INT_MAX && i < tram.departuresA[day].size())
    {
        Time t = tram.departuresA[day][i] + Time(0, timeToStop);
        // each line represents a different hour of departure
        if (t.hours == hour)
        {
            line += t.toString(true) + "\t";
        }
        else
        {
            result += line + " \n";
            hour = t.hours;
            line = std::to_string(hour) + "\t";
        }
        i++;
    }
    // the same as above but for departures from start B
    timeToStop = tram.timesB[stopName];
    if (timeToStop != INT_MAX)
    {
        result += "Direction: " + tram.startA + " \n";
        result += "Hour\tMinute\t \n";
    }
    hour = (tram.departuresB[day][0] + Time(0, timeToStop)).hours;
    line = std::to_string(hour) + "\t";
    i = 0;
    while (timeToStop != INT_MAX && i < tram.departuresB[day].size())
    {
        Time t = tram.departuresB[day][i] + Time(0, timeToStop);
        if (t.hours == hour)
        {
            line += t.toString(true) + "\t";
        }
        else
        {
            result += line + " \n";
            hour = t.hours;
            line = std::to_string(hour) + "\t";
        }
        i++;
    }
    return result;
}

std::vector<Time> Data::get_times(std::string s)
{
    std::vector<Time> times;
    auto tokens = getTokens(s, ' ');
    for (std::string token : tokens)
    {
        auto parts = getTokens(token, ':');
        int mins = std::stoi(parts[0]);
        int hrs = std::stoi(parts[1]);
        times.push_back(Time(mins, hrs));
    }
    return times;
}

std::vector<std::string> Data::getTokens(const std::string& line, char d)
{
    std::string str;
    std::stringstream ss(line);
    std::vector<std::string> tokens;
    while (std::getline(ss, str, d))
    {
        tokens.push_back(str);
    }
    return tokens;
}

std::string Data::fillFirstCol(std::string s)
{
    int x = stopColumn - s.size();
    std::string result = "";
    for (int i = 0; i < x; i++)
    {
        result += " ";
    }
    return result + "\t";
}

std::string Data::daytypeToString(day_type d)
{
    if (d == workday)
        return "workday";
    if (d == saturday)
        return "saturday";
    if (d == sunday)
        return "sunday";
}

std::map<Time, std::string> Data::find(Tram tram, std::string stop, Time t, day_type day)
{
    int timeToStopFromA = tram.timesA[stop];
    int timeToStopFromB = tram.timesB[stop];
    std::map<Time, std::string> times;
    size_t i = 0;
    size_t j = 0;
    // add next time until found ten departures or at end of possible departures
    while (i < tram.departuresA[day].size() && j < tram.departuresB[day].size() && times.size() < 10)
    {
        Time timeA = tram.departuresA[day][i] + Time(0, timeToStopFromA);
        Time timeB = tram.departuresB[day][j] + Time(0, timeToStopFromB);
        if (timeA >= t and timeA.minutes != INT_MAX)
            times.insert_or_assign(timeA, tram.startB);
        if (timeB >= t and timeB.minutes != INT_MAX)
            times.insert_or_assign(timeB, tram.startA);
        i++;
        j++;
    }
    return times;
}

std::string Data::stop_time_departures(std::string stopName, day_type day, Time t)
{
    std::string result;
    std::list<int>& tramsAtStop = stops.at(stopName);
    std::multimap<Time, std::pair<int, std::string>> possibleTimes;
    // for each tram that stops at the given stop find the ten closest upcoming departures and add to sorted possibleTimes map
    for (int tramNumber : tramsAtStop)
    {
        auto times = find(trams[tramNumber], stopName, t, day);
        for (auto entry : times)
        {
            possibleTimes.insert(std::make_pair(entry.first, std::make_pair(tramNumber, entry.second)));
        }
    }
    int printed = 0;
    if (possibleTimes.size() == 0)
    {
        result += "No departures from " + stopName + " after " + t.toString() + " \n";
        return result;
    }
    result += "Time\tTram\tDirection\t \n";
    // takes first ten departures possibleTimes
    for (auto departure : possibleTimes)
    {
        if (printed >= 10)
            return result;
        result += departure.first.toString() + "\t" +
            std::to_string(departure.second.first) + "\t" + departure.second.second + " \n";
        printed++;
    }

    return result;
}

std::vector<std::string> Data::get_trams_vector()
{
    std::vector<std::string> result;
    for (auto it = trams.begin(); it != trams.end(); it++)
    {
        result.push_back(std::to_string((*it).first));
    }
    
    return result;
}

std::vector<std::string> Data::get_stops_vector()
{
    std::vector<std::string> result;
    for (auto it = stops.begin(); it != stops.end(); it++)
    {
        result.push_back((*it).first);
    }
    std::sort(result.begin(), result.end());
    return result;
}

std::vector<std::string> Data::get_days_vector()
{
    std::vector<std::string> result;
    result.push_back(daytypeToString(workday));
    result.push_back(daytypeToString(saturday));
    result.push_back(daytypeToString(sunday));
    return result;
}