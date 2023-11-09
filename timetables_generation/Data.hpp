#pragma once

#include <string>
#include <vector>
#include <iostream>
#include <fstream>
#include <sstream>
#include <unordered_map>
#include <map>

#include "Time.hpp"

class Data
{
public:
    enum day_type
    {
        workday,
        saturday,
        sunday,
    };

    struct Tram
    {
        std::string startA;
        std::string startB;
        std::unordered_map<day_type, std::vector<Time>> departuresA;    // departure times from strartA
        std::unordered_map<day_type, std::vector<Time>> departuresB;    // departure times from startB
        std::vector<std::string> stops;                                 // vector of all stops, in order from startA to startB
        std::unordered_map<std::string, int> timesA;                    // how long it takes to get from startA to given stop (string) in minutes (int)
        std::unordered_map<std::string, int> timesB;                    // same as above but from startB
    };

    // adds tram route (specified in file) to application
    void addTram(std::string filename);

    // calculates and formats full timetable for a given tram on specified type of day
    std::string tram_full_timetable(int tramNum, day_type day);

    // calculates and formats all departures from stop for a specified tram and type of day
    std::string tram_stop_timetable(int tramNum, std::string stopName, day_type day);

    // calculates first ten departures starting at time t at specified stop and day type
    std::string stop_time_departures(std::string stopName, day_type day, Time t);

    // following three methods return vectors which contain options for corresponding wxChoice "dropdown" menus
    std::vector<std::string> get_trams_vector();

    std::vector<std::string> get_stops_vector();

    std::vector<std::string> get_days_vector();

    std::vector<day_type> daytypes = { workday, saturday, sunday };

private:
    // splits string of times XX:XX seperated by single space into a vector of times 
    std::vector<Time> get_times(std::string s);

    // splits string into vector of substrings using delimiter, char d
    std::vector<std::string> getTokens(const std::string& line, char d);

    // determines how much space to add after stop string to line up neatly with longest stop string
    std::string fillFirstCol(std::string s);

    // converts day type to string
    std::string daytypeToString(day_type d);

    // finds first ten departures of specified tram at stop on day starting at time t
    std::map<Time, std::string> find(Tram tram, std::string stop, Time t, day_type day);

    std::unordered_map<std::string, std::list<int>> stops; //what trams stop at given stop
    std::unordered_map<int, Tram> trams; //tram number and its data
    int stopColumn; //how much space first column should take up

};

