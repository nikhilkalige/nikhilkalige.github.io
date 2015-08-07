Title: Google Calendar Birthday Notifications for Android Contacts
Category: Javascript
Tags: Google Calendar, Android, Javascript
Date: 2015-08-07
Slug: google-calendar-birthday-notifications
Summary: Add notifications to birthday events in google calendar


Android has a nice feature of synchronizing birthdays that you have included in the contacts.  It creates a new calendar named **Birthdays** which includes all the birthdays from the contacts as well as from the **Google+** circle if you want. But my problem is that it does not allow you to add notifications for those dates.

I was thinking whether you could write a script to access the calendar and make some changes and voilà, I found out that google has a nice feature called [Appscripts](https://developers.google.com/apps-script/%20%22App%20scripts) that allows you to write scripts that run on the google cloud. So I wrote a small script that adds this feature.

### Setup
All you need to do to get started is go to [https://script.google.com/](https://script.google.com/) and create a new blank project. Then you would need to give appropriate permissions to the project so it can access your data. To do that click *Resources -> Advanced Google Services* and then enable *Calendar API*. You would also need to enable access in *[Google Developers Console](https://console.developers.google.com) too.

### Calendar API
The overall logic is to create a new calendar and clone the events from the Birthdays calendar into it. Also you need to add notifications and make it a recurring event.

```javascript
function addBdayNotifications() {
    var bdayCal, bdayNotifyCal;

    var calendars = CalendarApp.getAllCalendars();

    for (var i = 0; i < calendars.length; i++) {
        if (calendars[i].getName() == "Birthday Notifications") bdayNotifyCal = calendars[i];
        if (calendars[i].getName() == "Birthdays") bdayCal = calendars[i];
    }

    if (bdayCal == undefined) return;

    if (bdayNotifyCal == undefined) {
        bdayNotifyCal = CalendarApp.createCalendar("Birthday Notifications");
        bdayNotifyCal.setHidden(true);
    }

    var currentYear = new Date().getFullYear();

    var fromDate = new Date(currentYear, 0, 1);
    var toDate = new Date(currentYear, 11, 31);

    var bdayEvents = bdayCal.getEvents(fromDate, toDate);
    var notifyEvents = bdayNotifyCal.getEvents(fromDate, toDate);

    // Maintain a list of event titles
    var notifyEventsTitle = [];
    for (i = 0; i < notifyEvents.length; i++) {
        notifyEventsTitle.push(notifyEvents[i].getTitle())
        if (i % 25 == 0) Utilities.sleep(1000);
    }

    var items = 0;
    bdayEvents.forEach(function(evt) {
        var status = createEvent(bdayNotifyCal, notifyEventsTitle,
            evt.getTitle(), evt.getStartTime());

        if (status) items++;
        if (items % 5 == 0) Utilities.sleep(1000);
    })

    Logger.log("%s events added to the calendar", items);
}

function createEvent(cal, eventList, title, time) {
    for (var i = eventList.length - 1; i >= 0; i--) {
        if (eventList[i] == title) return false;
    }

    cal.createAllDayEventSeries(title, time,
        CalendarApp.newRecurrence().addYearlyRule(), {})
        .setGuestsCanInviteOthers(false)
        .setGuestsCanModify(false)
        .setGuestsCanSeeGuests(false)
        .addPopupReminder(2 * 60);

    return true;
}

function createTrigger() {
    ScriptApp.newTrigger("addBdayNotifications")
        .timeBased()
        .everyDays(1)
        .create();
}
```

The above code is pretty straightforward. Initially you look for the necessary calendars from your list of owned calendars. You then create a new calendar for notifications if one doesn't exist already. After that create a list of birthdays present in the current year from both the calendars. Then its all about looping over the event list and creating a new one if one doesn't exist.

During the event creation, you add an yearly recursion rule and set a pop-up reminder.

You would probably not want to trigger the code to run every time you add a contact. So we will make use of *[Triggers](https://developers.google.com/apps-script/guides/triggers/)* feature. It would have been nice if a trigger could be set on new event creation, but I could not find anything like that, therefore I added a daily trigger.

You could run in to a problem where google complains that you are creating too may events, in order to go around that I have added some delays but I haven't arrived at an optimum solution for that.

Finally the last thing to do is to hide the calendar using `.setHidden(true)`. This is nice feature that hides the calendar in the UI and solves the problem of having multiple birthdays on your calendar.


### Conclusion
This is not a bullet proof solution for the problem. I would love to know if its possible to do this in different manner without using scripts.


