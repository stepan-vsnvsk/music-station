let tracklist = JSON.parse(document.getElementById('tracklist_id').textContent);
_ = tracklist.shift();

document.getElementById('player').addEventListener("ended", function() {    
    if (typeof tracklist != "undefined" &&
        tracklist != null &&
        tracklist.length != null &&
        tracklist.length > 0) {
        this.src = tracklist.shift();
        this.play();
    } else {
        this.pause();
    }

});
