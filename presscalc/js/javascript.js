function solve(form)
{
	var pt_name_first = form.pt_name_first.value;
	var pt_name_last = form.pt_name_last.value;
	var pt_id = form.pt_id.value;
	var date = form.date.value;
	var time = form.time.value;
	var caregiver_id = form.caregiver_id.value;
	var ed_id = form.ed_id.value;
	var ambulance_id = form.ambulance_id.value;
	var pt_age = form.pt_age.value;
	var is_nursing = form.is_nursing.value;
	var is_sick = form.is_sick.value;
	var is_febrile = form.is_febrile.value;
	var sbp = form.sbp.value;
	var o2sat = form.o2sat.value;
	var points = 0;
	var flag = false;

	// console.log("Patient name: " + pt_name);
	// console.log("Patient ID: " + pt_id);
	// console.log("Date & Time: " + datetime);
	// console.log("Caregiver ID: " + caregiver_id);
	// console.log("ED ID: " + ed_id);
	// console.log("Ambulance ID: " + ambulance_id);
	console.log("Age: " + pt_age);
	console.log("From a nursing home?: " + is_nursing);
	console.log("Are they sick?: " + is_sick);
	console.log("Are they febrile?: " + is_febrile);

if (is_sick) {
    points += 3;
}

if (is_nursing) {
    points += 4;
}

// patient age

if (pt_age == "middle") {
    points += 4;
}

else if (pt_age == "old") {
    points += 2;
}

if (is_febrile) {
    points += 3;
}

// calculate points for systolic blood pressure

if (sbp >= 90 && sbp < 100) {
    points += 1;
}

else if (sbp >= 80 && sbp < 90) {
    points += 2;
}

else if (sbp >= 70 && sbp < 80) {
    points += 3;
}

else if (sbp >= 60 && sbp < 70) {
    points += 4;
}

else if (sbp < 60 && sbp > 1) {
    points += 5;
}

// calculate points for oxygen saturation

if (o2sat >= 80 && o2sat < 90) {
    points += 1;
}

else if (o2sat >= 70 && o2sat < 80) {
    points += 3;
}

else if (o2sat >= 60 && o2sat < 70) {
    points += 4;
}

else if (o2sat < 60 && o2sat > 1) {
    points += 5;
}

var sigma = -4.71 + (0.393 * points)
var phat = 1 / (1 + Math.exp(-sigma))

console.log("PreSS score: " + points + " points");
console.log("Risk of severe sepsis: " + phat * 100);

var w = window.open('', '', 'width=400,height=400,resizeable,scrollbars');
w.document.write("Risk of severe sepsis: " + phat * 100 + '<br>' + "PreSS score: " + points + " points");
w.document.close();

}
