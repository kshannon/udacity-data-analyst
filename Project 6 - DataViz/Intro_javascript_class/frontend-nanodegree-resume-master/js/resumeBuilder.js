
var position = "Clarity from Confusion";
var formattedPosition = HTMLheaderRole.replace("%data%", position);
$("#header").prepend(formattedPosition);

var k_name = "Kyle Shannon";
var formattedName = HTMLheaderName.replace("%data%", name);
$("#header").prepend(formattedName);


/*
education contains an array of schools. Each school object in schools contains a
name, location, degree, majors array, dates attended and a url for the school's
website. education also contains an onlineCourses array. Each onlineCourse
object in onlineCourses should contain a title, school, dates attended and a url
for the course.
*/

var education = {
	"Schools" : [
		{
			"name" : "ucsd",
			"location" : "SD",
			"major" : ["neuro"]
		},
		{
			"name" : "Udacity",
			"Head_Master" : "Sebastian",
			"FavStudent" : "Sarahhh"
		}
	]
};

/*
bio contains a name, role, welcomeMessage, contacts object and skills array. The
contacts object should contain (but doesn't have to) a mobile number, email
address, github username, twitter handle and location.
*/
var bio = {
	"position" : position,
	"name" : k_name,
	"contact_info" : {
					"phone" : "858.752.3563",
					"email" : "dsfdfd@hgd.com"
				},
	"age" : 26,
	"welcome_message" : "OHAHAHAHA",
	"skills" : ["pypy", "ml", "art", "neuro"]
};


/* work contains an array of jobs. Each job object in jobs should contain an
employer, title, location, dates worked and description.
*/
var work = {
	"jobs" : [
		{
			"employer" : "booz",
			"loc" : "SD",
			"title" : "data"
		},
		{
			"employer" : "BYB",
			"loc" : "MI",
			"title" : "neuro-wizard-mancer"
		}
	]
};


/*
projects contains an array of projects. Each project object in projects should
contain a title, dates worked, description, and an images array with URL strings
for project images.
*/
var projects = {
	"project" : [
		{
			"title" : "enron",
			"description" : "Identified POIs using ML techniques."
		},
		{
			"title" : "Open Street Map",
			"Description" : "data munged large XML file of Seattle Street Map data."
		}

	]
};


// for..in   vs   for..of

/*if (bio.skills.length > 0)
{
	$("#header").append(HTMLskillsStart);
	

	for (var skill in bio.skills)
	{
		formattedSkill = HTMLskills.replace("%data%", bio.skills[skill]);
		$("#skills").append(formattedSkill);
	}
}*/

if (bio.skills.length > 0)
{
	$("#header").append(HTMLskillsStart);
	

	for (var skill of bio.skills)
	{
		formattedSkill = HTMLskills.replace("%data%", skill);
		$("#skills").append(formattedSkill);
	}
}

$(document).click(function(loc)
{
	//console.log(loc);
	logClicks(loc.pageX, loc.pageY);
});

$("#main").append(internationalizeButton)
function inName(name)
{
	name = bio.name;
	//alert(name);
	var nameArray = name.split(" ");
	nameArray[1] = nameArray[1].toUpperCase();
	var internationaName = nameArray.join(" ");
	return internationaName;
};

projects.display = function()
{
	$("#projects").append(HTMLprojectStart);
	
	for(var item of projects.project)
	{
		formattedProject = HTMLproject.replace("%data%", project.project);
		$("#projects").append(formattedProject);
	}
}

projects.display()

// Misc Code from Class:

/*
$("#main").append(["kyle shannon<br/>"]);
[string].replace([old],[new])

var awesome_thoughts = "I am Kyle and I might be awesome...";
console.log(awesome_thoughts);

var fun_thoughts = awesome_thoughts.replace("awesome", "fun");

console.log(fun_thoughts);

 $("#main").append([fun_thoughts]);
*/


/* from class....

var weirdObject = {
    "property": "Time for an astronomy lesson!",
    "property1": "Cameron's minor in college was astronomy",
    "property-2": "The 4 Galilean largest moons of Jupiter are:",
    "property 3": "Io, Ganymede, Callisto, Europa",
    "property$": "Saturn's moon Enceladus has liquid water ocean under its icy surface",
    " property": "The Sun contains 99.87% of the mass of the entire solar system",
    "property()": "There are 5 dwarf planets in our solar system:",
    "property[]": "Pluto, Ceres, Eris, Haumea, Makemake",
    "8property": "Mars has two tiny moons: Phobos and Deimos"
};

// Use console.log() to figure out if dot and/or bracket notation
// will work to access the properties below. Mark true if you can use dot/bracket
// notation to access the property, otherwise mark false.

// For example, uncomment the line below to see if you can use dot notation to access `property1`.
// console.log(weirdObject.property1);

// I'll give you the first answer. The rest are set to false. Try out each property and
// if you can use dot or bracket notation to access it, change the answer to true!

// property
console.log("property");
console.log(weirdObject.property);
console.log(weirdObject["property"]);
var dotNotation0 = true;
var bracketNotation0 = true;



// property1
console.log("property1");
console.log(weirdObject.property1);
console.log(weirdObject["property1"]);
var dotNotation1 = true;
var bracketNotation1 = true;

// property-2
console.log("property-2");
console.log(weirdObject.property-2);
console.log(weirdObject["property-2"]);
var dotNotation2 = false;
var bracketNotation2 = true;

// property 3
console.log("property 3");
//console.log(weirdObject.property 3);
console.log(weirdObject["property 3"]);
var dotNotation3 = false;
var bracketNotation3 = true;

// property$
console.log("property$");
console.log(weirdObject.property$);
console.log(weirdObject["property$"]);
var dotNotation4 = true;
var bracketNotation4 = true;

// *space*property
console.log("*space*property");
//console.log(weirdObject.*space*property);
console.log(weirdObject["*space*property"]);
var dotNotation5 = false;
var bracketNotation5 = true;

// property()
//console.log("property()");
//console.log(weirdObject.property());
//console.log(weirdObject["property()"]);
var dotNotation6 = false;
var bracketNotation6 = false;

// property[]
console.log("property[]");true
//console.log(weirdObject.property[]);
console.log(weirdObject["property[]"]);
var dotNotation7 = false;
var bracketNotation7 = true;

// 8property
console.log("8property");
//console.log(weirdObject.8property);
console.log(weirdObject["8property"]);
var dotNotation8 = false;
var bracketNotation8 = true;

*/

/*function locationizer(work_obj) 
{
    var loc_array = [];
    for (var job in work_obj.jobs)
    {
        loc_array.push(work_obj.jobs[job].location);
    }
    return loc_array;
}*/







