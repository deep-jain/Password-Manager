//display modal on click

const modalWrapper = document.querySelector(".modals-wrapper");
if (modalWrapper){
	function displayModal(id){
		const modal = document.getElementById(id);
		modalWrapper.style.display = "flex";
		modal.style.display = "flex";
		//close modal
		const close = document.getElementById("close-modal");
		close.addEventListener("click", () =>{
			modalWrapper.style.display = "none";
			modal.style.display = "none";
		})
	}
}


//copy to clipboard
const copies = document.querySelectorAll(".copy");
copies.forEach(copy =>{
	copy.onclick = () =>{
		let elementToCopy = copy.previousElementSibling;
		elementToCopy.select();
		document.execCommand("copy");
	}
})
