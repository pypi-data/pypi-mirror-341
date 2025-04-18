(function () {
    function randint (a, b) {
        return Math.floor(a + (Math.random() * (b-a+1)));
    }
    function colortitle () {
        var title = document.querySelector("h1"),
            text = title.innerHTML,
            p, l, span;
    
        function shuffle () {
            title.innerHTML = "";
            p = 0;
            while (p < text.length) {
                l = randint(1, 4);
                span = document.createElement("span");
                span.innerHTML = text.substring(p, p+l);
                if (randint(1, 3) != 3) {
                    span.style.background = "hsl("+randint(0, 360)+",100%,80%)";
                }
                title.appendChild(span);
                p += l;
            }
        }
        shuffle();
        // window.setInterval(shuffle, 10000);
    }
    document.addEventListener("DOMContentLoaded", colortitle);
})();
