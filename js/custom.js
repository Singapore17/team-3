var benificiaries = {
	1: {
	"abc":{
	"baby_food_baby_cereals" : 0,
	"baby_food_baby_milk" : 0,
	"baking_needs_premix_powder" : 0,
	"beverages_adult_milk_powder" : 0,
	"beverages_water" : 0,
	"canned_food_vegetarian" : 0,
	"condiments_vinegar" : 0,
	"condiments_peanut_butter" : 0,
	"condiments_sugar" : 0,
	"condiments_almond_syrup" : 0,
	"condiments_maple_syrup" : 0,
	"dried_food_grains" : 0,
	"dried_food_white_fungus" : 0,
	"preserved_vegetables" : 0,
	"snacks_bars" : 0,
	"snacks_sweets" : 0,
	"staples_cereal" : 0,
	"staples_noodles" : 0,
	"staples_pasta" : 0,
	"staples_rice" : 0,
	}},
	2: {
	"def":{
	"baby_food_baby_cereals" : 0,
	"baby_food_baby_milk" : 0,
	"baking_needs_premix_powder" : 0,
	"beverages_adult_milk_powder" : 0,
	"beverages_water" : 0,
	"canned_food_vegetarian" : 0,
	"condiments_vinegar" : 0,
	"condiments_peanut_butter" : 0,
	"condiments_sugar" : 0,
	"condiments_almond_syrup" : 0,
	"condiments_maple_syrup" : 0,
	"dried_food_grains" : 0,
	"dried_food_white_fungus" : 0,
	"preserved_vegetables" : 0,
	"snacks_bars" : 0,
	"snacks_sweets" : 0,
	"staples_cereal" : 0,
	"staples_noodles" : 0,
	"staples_pasta" : 0,
	"staples_rice" : 0,
	}},
};
var inventory = {
	"baby_food_baby_cereals" : 4,
	"baby_food_baby_milk" : 10,
	"baking_needs_premix_powder" : 10,
	"beverages_adult_milk_powder" : 5,
	"beverages_water" : 8,
	"canned_food_vegetarian" : 8,
	"condiments_vinegar" : 8,
	"condiments_peanut_butter" : 8,
	"condiments_sugar" : 2,
	"condiments_almond_syrup" : 3,
	"condiments_maple_syrup" : 4,
	"dried_food_grains" : 10,
	"dried_food_white_fungus" : 1,
	"preserved_vegetables" : 3,
	"snacks_bars" : 2,
	"snacks_sweets" : 20,
	"staples_cereal" : 8,
	"staples_noodles" : 12,
	"staples_pasta" : 4,
	"staples_rice" : 10,
};


function login() {
	var uname = document.getElementById('exampleInputEmail1').value;
	var password = document.getElementById('exampleInputPassword1').value;

	if (uname="admin" && password=="admin"){
		window.location.replace('admin.html');
		$("#loginError").css("display", "none");
	}
	else if (uname="abc" && password=="abc"){
		window.location.replace('user.html');
		$("#loginError").css("display", "none");
	}
	else{
		$("#loginError").css("display", "block");
	}
}

function matching(){
}