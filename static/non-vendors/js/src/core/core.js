class PastagCoreWebController {
    constructor(passedConfig){
      // Always call the pastagInit function when extending from this component
      // Common things that we do on init
  
      // Handles the config for pastag core controller
      const defaults = {
        wait: true
      };
  
      // assign empty then assign the defaults, and finally assign the passed options
      let coreConfig = Object.assign({}, defaults, passedConfig);
  
      // Wait for everything to be loaded before firing the initialization
      if(coreConfig.wait == true){
        document.addEventListener("DOMContentLoaded", () => {
          this.pcInit();
        });
      }else{
        this.pcInit();
      }
    }
  
    pcInit () {
      this.pcSetUpProperties();
      this.pcBindEvent();
    };
  
  
    pcGetUrlParmas(){
      return new URLSearchParams(window.location.search);
    }
  
    pcSetUpProperties(){ return false };
  
    // TODO: Find a better way to implement this
    // Just return false if no bind event exists
    pcBindEvent(){ return false };
  
    pcDefaultFailedRequestResponse(request){
       // We reached our target server, but it returned an error
       console.log(request.response);
    }
  
  }
  
  export default PastagCoreWebController;