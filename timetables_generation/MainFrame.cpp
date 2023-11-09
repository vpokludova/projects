#include "MainFrame.hpp"

#include <wx/wx.h>
#include "Data.hpp"

enum IDs {
	BUTTON_ID = 2,
	TRAM_CHOICE_ID = 3,
	STOP_CHOICE_ID = 4,
	DAY_CHOICE_ID = 5,
	TIME_HR_CHOICE_ID = 6,
	TIME_MIN_CHOICE_ID = 7,
	ACTION_CHOICE_ID = 8
};

wxBEGIN_EVENT_TABLE(MainFrame, wxFrame)
	EVT_BUTTON(BUTTON_ID, MainFrame::OnButtonClicked)
wxEND_EVENT_TABLE()

MainFrame::MainFrame(const wxString& title) : wxFrame(nullptr, wxID_ANY, title)
{
	panel1 = new wxPanel(this, wxID_ANY, wxPoint(0, 0), wxSize(800, 100));
	panel2 = new wxPanel(this, wxID_ANY, wxPoint(0, 100), wxSize(800, 500));

	enterButton = new wxButton(panel1, BUTTON_ID, "Enter", wxPoint(610, 45), wxSize(100, 35));

	tramLabel = new wxStaticText(panel1, wxID_ANY, "Tram", wxPoint(20, 30));
	stopLabel = new wxStaticText(panel1, wxID_ANY, "Stop", wxPoint(90, 30));
	dayLabel = new wxStaticText(panel1, wxID_ANY, "Day", wxPoint(210, 30));
	timeLabel = new wxStaticText(panel1, wxID_ANY, "Time", wxPoint(280, 30));
	actionLabel = new wxStaticText(panel1, wxID_ANY, "Action", wxPoint(390, 30));

	// drop down for hour options
	for (int i = 1; i <= 24; i++)
	{
		hoursChoices.Add(std::to_string(i));
	}
	timeHrChoice = new wxChoice(panel1, TIME_HR_CHOICE_ID, wxPoint(280, 50), wxSize(40, -1), hoursChoices);
	timeHrChoice->Select(0);

	// drop down for minute options
	for (int i = 0; i <= 59; i++)
	{
		minsChoices.Add((Time(0, i)).toString(true));
	}
	timeMinChoice = new wxChoice(panel1, TIME_MIN_CHOICE_ID, wxPoint(330, 50), wxSize(40, -1), minsChoices);
	timeMinChoice->Select(0);

	// action choices correspond to corresponding "action" methods in data class
	actChoices.Add("Full timetable for chosen tram");
	actChoices.Add("Departures for given stop and tram");
	actChoices.Add("Departures for given stop and time");
	actionChoice = new wxChoice(panel1, ACTION_CHOICE_ID, wxPoint(390, 50), wxSize(200, -1), actChoices);
	actionChoice->Select(0);

	out = new wxTextCtrl(panel2, wxID_ANY, wxEmptyString, wxPoint(5, 5), wxSize(780, 490), wxTE_MULTILINE | wxVERTICAL | wxTE_READONLY | wxHSCROLL);
	out->SetFont(wxFont(10, wxFONTFAMILY_MODERN, wxFONTSTYLE_NORMAL, wxFONTWEIGHT_BOLD));

	d = Data();
	d.addTram("linka_8.txt");
	d.addTram("linka_1.txt");
	d.addTram("linka_25.txt");
	auto trams = d.get_trams_vector();
	setTramChoices(trams);
	auto stops = d.get_stops_vector();
	setStopsChoices(stops);
	auto days = d.get_days_vector();
	setDaysChoices(days);
}

void MainFrame::setTramChoices(const std::vector<std::string>& t)
{
	for (std::string tram : t)
	{
		tramChoices.Add(tram);
	}
	tChoice = new wxChoice(panel1, TRAM_CHOICE_ID, wxPoint(20, 50), wxSize(50, -1), tramChoices);
	tChoice->Select(0);
	return;
}

void MainFrame::setStopsChoices(const std::vector<std::string>& t)
{
	for (std::string stop : t)
	{
		stopChoices.Add(stop);
	}
	sChoice = new wxChoice(panel1, STOP_CHOICE_ID, wxPoint(90, 50), wxSize(100, -1), stopChoices);
	sChoice->Select(0);
	return;
}

void MainFrame::setDaysChoices(const std::vector<std::string>& t)
{
	for (std::string day_type : t)
	{
		daytypeChoices.Add(day_type);
	}
	dChoice = new wxChoice(panel1, DAY_CHOICE_ID, wxPoint(210, 50), wxSize(50, -1), daytypeChoices);
	dChoice->Select(0);
	return;

}

void MainFrame::setOuput(const std::string& t)
{
	out->Clear();
	out->AppendText(t);
}

void MainFrame::OnButtonClicked(wxCommandEvent& evt)
{
	// get current selections of other dropdown menus
	int tramIndex = tChoice->GetCurrentSelection();
	int tram = std::stoi(std::string(tramChoices[tramIndex].mb_str()));
	int stopIndex = sChoice->GetCurrentSelection();
	std::string stop = std::string(stopChoices[stopIndex].mb_str());
	int dayIndex = dChoice->GetCurrentSelection();
	
	int hour = (timeHrChoice->GetCurrentSelection()) + 1;
	int minutes = timeMinChoice->GetCurrentSelection();

	// action selected by user
	int actionIndex = actionChoice->GetCurrentSelection();

	std::string result;
	// call corresponding method in data class
	if (actionIndex == 0)	// Full timetable for given stop
	{
		result = d.tram_full_timetable(tram, d.daytypes[dayIndex]);
	}
	else if (actionIndex == 1) // Departures for given stop and tram
	{
		result = d.tram_stop_timetable(tram, stop, d.daytypes[dayIndex]);
	}
	else if (actionIndex == 2) // Departures for given stop and time
	{
		result = d.stop_time_departures(stop, d.daytypes[dayIndex], Time(hour, minutes));
	}
	
	setOuput(result);

}