CodeMirror.defineMode("pseudocode", function() {
    return {
      token: function(stream, state) {
        if (stream.match("//", false)) {
          stream.skipToEnd(); // Siirry rivin loppuun
          return "comment"; // Määrittele tämä teksti kommentiksi
        }
        if (stream.match("IF", false)) {
          stream.match("IF");
          return "keyword";
        } else if (stream.match("THEN", false)) {
          stream.match("THEN");
          return "keyword";
        } else if (stream.match("ELSE", false)) {
          stream.match("ELSE");
          return "keyword";
        }
        while (stream.next() != null && !stream.match("//", false) && 
               !stream.match("IF", false) && 
               !stream.match("THEN", false) && 
               !stream.match("ELSE", false)) {}
        return null;
      }
    };
  });



// Määritellään algoritmien vaativuuden laskennan mode
CodeMirror.defineMode("complexityAnalysis", function() {
    return {
        token: function(stream, state) {
            if (stream.match("//", false)) {
                stream.skipToEnd();
                return "comment";
            }
            if (stream.match("BIG-O", false)) {
                stream.match("BIG-O");
                return "keyword";
            } else if (stream.match("CONSTANT", false)) {
                stream.match("CONSTANT");
                return "keyword";
            } else if (stream.match("LINEAR", false)) {
                stream.match("LINEAR");
                return "keyword";
            } else if (stream.match("QUADRATIC", false)) {
                stream.match("QUADRATIC");
                return "keyword";
            } else if (stream.match("LOGARITHMIC", false)) {
                stream.match("LOGARITHMIC");
                return "keyword";
            } else if (stream.match("FOR", false)) {
                stream.match("FOR");
                return "loop";
            } else if (stream.match("WHILE", false)) {
                stream.match("WHILE");
                return "loop";
            } else if (stream.match("IF", false)) {
                stream.match("IF");
                return "condition";
            } else if (stream.match("ELSE", false)) {
                stream.match("ELSE");
                return "condition";
            }
            while (stream.next() != null && !stream.match("//", false) && 
                   !stream.match("BIG-O", false) &&
                   !stream.match("CONSTANT", false) &&
                   !stream.match("LINEAR", false) &&
                   !stream.match("QUADRATIC", false) &&
                   !stream.match("LOGARITHMIC", false) &&
                   !stream.match("FOR", false) &&
                   !stream.match("WHILE", false) &&
                   !stream.match("IF", false) &&
                   !stream.match("ELSE", false)) {}
            return null;
        }
    };
});
