import PastagWebController from '../core/core.js';

class loginController extends PastagWebController{
    constructor(){
        super();
    }

    pcInit(){
        super.pcInit();

        document.querySelector(".container").classList.add("in");

        // waits for the image background to load
        const src = getComputedStyle(document.querySelector(".login-background"))['background-image'];
        if(src !== null){
            const url = src.match(/\((.*?)\)/)[1].replace(/('|")/g,'');
            let img = new Image();
            img.onload = function() {
                document.querySelector(".login-background").classList.add("in");
            }
            img.src = url;
            if (img.complete) img.onload();
        }else{
            document.querySelector(".login-background").classList.add("in");
        }
    }
}

let page = new loginController();