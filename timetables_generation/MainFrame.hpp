#pragma once
#include <wx/wx.h>
#include "Data.hpp"

class MainFrame : public wxFrame
{
public:
	MainFrame(const wxString& title);	
	
	// following three methods add all choices from Data class to wxChoice objects in application
	void setTramChoices(const std::vector<std::string>& t);

	void setStopsChoices(const std::vector<std::string>& t);

	void setDaysChoices(const std::vector<std::string>& t);

	// replaces panel2 with input string
	void setOuput(const std::string& t);

private:
	Data d;

	wxPanel* panel1;	// contains all dropdown (wxChoice) menus
	wxPanel* panel2;	// contains output

	wxButton* enterButton;

	wxStaticText* tramLabel;
	wxStaticText* stopLabel;
	wxStaticText* dayLabel;
	wxStaticText* timeLabel;
	wxStaticText* actionLabel;

	wxArrayString tramChoices;
	wxArrayString stopChoices;
	wxArrayString daytypeChoices;
	wxArrayString hoursChoices;
	wxArrayString minsChoices;
	wxArrayString actChoices;

	wxChoice* tChoice;
	wxChoice* sChoice;
	wxChoice* dChoice;
	wxChoice* timeHrChoice;
	wxChoice* timeMinChoice;
	wxChoice* actionChoice;

	wxTextCtrl* out;

	void OnButtonClicked(wxCommandEvent& evt);		

	wxDECLARE_EVENT_TABLE();
};

