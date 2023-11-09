#include "App.hpp"
#include "MainFrame.hpp"
#include "Data.hpp"
#include <wx\wx.h>

bool App::OnInit()
{
	MainFrame* mainFrame = new MainFrame("Tram Timetables");
	mainFrame->SetClientSize(800, 600);
	mainFrame->Center();
	mainFrame->Show();
	return true;
}

wxIMPLEMENT_APP(App);