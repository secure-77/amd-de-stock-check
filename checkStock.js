var list = document.getElementsByClassName("direct-buy");

for (let item of list) {
	
	var productName = item.getElementsByClassName("shop-title")[0].innerText;
	var availibility = item.getElementsByClassName("shop-links")[0].innerText;

	if (productName == 'AMD RYZEN™ 9 5900X Processor' 
	||  productName == 'AMD RYZEN™ 5 5600X Processor' 
	||  productName == 'AMD Radeon™ RX 6800 XT Graphics')
	{
		console.log(productName);
		if (availibility != 'Out of Stock') {
			console.log("availibe");
			alert(productName + " availibe!");
		} else {
			console.log(availibility);
		}	
	}
}