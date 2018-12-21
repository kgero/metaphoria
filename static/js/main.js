

var concrete = ["bed", "horse", "bell", "book", "ship", "wing", "wood", "room", "mouth", "storm", "town", "silver", "stream", "dust", "color", "side", "state", "ear", "sand", "grass", "rose", "blood", "girl", "ring", "wine", "garden", "brain", "wave", "mist", "dawn", "breath", "spring", "nation", "finger", "hair", "rock", "breast", "window", "snow", "body", "ground", "stone", "flame", "shadow", "line", "path", "king", "darkness"];
//slimmed concrete list
concrete = ["horse","finger","book","line","wood","hair","bed","king","bell",
            "window","ring","mouth","sand","silver","wine","rock","wing","snow",
            "ear","ship","garden","room","stone","storm","town","stream",
            "shadow"];
var poetic = ["loss", "confusion", "faith", "freedom", "grace", "hate", "jealousy", "love", "spring", "unity", "consciousness", "soul", "melancholy", "calmness", "death", "fear", "friendship", "gratitude", "hope", "joy", "nature", "religion", "sadness", "suffering", "vanity", "happiness", "surrender", "anger", "compassion", "envy", "forgiveness", "god", "grief", "immortality", "life", "peace", "remembrance", "silence", "spirituality", "truth", "war", "bitterness", "violence"];

var metaphor = {};

var repeat_expand = 0;
var prev_expand = '';
var template = {};

function create_metaphor(w1, w2) {
  if (metaphor.hasOwnProperty('c')) {
    metaphor.prev = metaphor.c;
  }
  var text = w1 + " is a " + w2;
  metaphor.p = w1; metaphor.c = w2; metaphor.t = text;
  var btn = $('<button>');
  btn.addClass('btn').addClass('btn-concrete').addClass('inline');
  var rand = $('<span class="glyphicon glyphicon-refresh btn-glyph"></span>');
  btn.append(' '+w2+'  ').append(rand);
  btn.click( function() {
    w2 = concrete[Math.floor(Math.random()*concrete.length)];
    create_metaphor(w1, w2);
    $('.idea').empty();
    get_ideas();
  });
  $('.btn-concrete').remove();
  $('.isa').text(' is a ');
  $('.metaphor').append(btn);
}

function build_compound(template) {
  var p = $("<p class='text-muted expand'>");
  p.append('&nbsp;&nbsp;&nbsp;&nbsp;');
  var t = template.template;
  t = t.replace(metaphor.p, "<strong><span class='p'>"+metaphor.p+"</span></strong>");
  t = t.replace(metaphor.c, "<strong><span class='c'>"+metaphor.c+"</span></strong>");
  
  var buttons = [];
  $.each(Object.keys(template), function(i, key) {
    if (key === 'template') { return true; }
    var b = $("<button type='button' class='btn btn-default btn-xs'>");
    template[key]['i'] = 0;
    b.html(template[key].fillings[template[key].i] + '&nbsp;<span class="glyphicon glyphicon-random tiny" aria-hidden="true"></span>');
    b.click( function () {
      template[key].i++;
      if (template[key].i >= template[key].fillings.length) { 
        template[key].i = 0; 
      }
      b.html(template[key].fillings[template[key].i] + '&nbsp;<span class="glyphicon glyphicon-random tiny" aria-hidden="true"></span>');
    });
    buttons.push([t.indexOf(key), b]);
  });

  if (template.hasOwnProperty('_p1')) {
    buttons.sort(function(a, b) {
      return (a[0] > b[0]) ? 1 : -1;
    });
    p.append(t.slice(0, buttons[0][0]));
    p.append(buttons[0][1]);
    $.each( buttons.slice(1), function( index, value) {
      p.append(t.slice(buttons[index][0]+3, value[0]));
      p.append(value[1]);
    });
    p.append(t.slice(buttons[buttons.length-1][0]+3, t.length));

  } else { p.append(t); }

  var c = $('<span class="glyphicon glyphicon-copy" aria-hidden="true">');
  c.click( function () {
    var p_add = $('<p>').text(p.text());
    console.log(p.text());
    console.log(p_add);
    $(".my-textarea").append(p_add);
  });
  c.hide();
  p.append('&nbsp;').append(c);
  p.hover( 
    function () { c.show(); }, 
    function () { c.hide(); });
  return p;
}

function get_ideas() {
  console.log('getting idea for ', metaphor.t);
  $('.idea').empty();
  console.log(metaphor);

  $.post('get_sug?', metaphor, function(json, status) {
    console.log(json);
    if (json.hasOwnProperty('error')) {
      $('.idea').append('<p>' + json.error);
      return;
    }
    var suggestions = json;
    $.each(suggestions, function(i, text) {
      var p = $("<p>");
      var s = $("<span>");
      s.append(plus).append('&nbsp;');
      var d = $("<div>");
      var c = $('<span class="glyphicon glyphicon-copy" aria-hidden="true">');
      c.hide();
      d.attr('value', text + "&nbsp;");
      s.hover( 
        function() { s.addClass('to-textbox'); },
        function() { s.removeClass('to-textbox'); });
      s.click( function() {
        var here = $(this).parent();
        if (s.hasClass('compounded')) {
          s.removeClass('compounded');
          $(this).children('.glyphicon').removeClass('glyphicon-minus').addClass('glyphicon-plus');
          here.next().remove();
          console.log('child:', $(this).children('.glyphicon'));
        } else {
          $(this).children('.glyphicon').removeClass('glyphicon-plus').addClass('glyphicon-minus');
          s.addClass('compounded');
          req = metaphor;
          req['s'] = text;
          // if (prev_expand == text) {
          //   console.log("change!");
          //   return;
          // }
          // else {repeat_expand = 0;}
          prev_expand = text;
          req['r'] = repeat_expand;
          console.log(req);        
          $.post('get_more?', req, function(json, status) {
            console.log(json);
            template = json;
            // $('.expand').remove();
            var c = build_compound(template);
            here.after(c);
          });
        }
      });
      p.hover( 
        function () { c.show(); }, 
        function () { c.hide(); });
      c.click( function () {
        var p_add = $('<p>').text(text);
        console.log(text);
        console.log(p_add);
        $(".my-textarea").append(p_add);
      });
      var newtext = text.replace(metaphor.p, "<span class='p'>"+metaphor.p+"</span>");
      newtext = newtext.slice(0,newtext.length - metaphor.c.length);
      newtext = newtext + "<span class='c'>"+metaphor.c+"</span>";
      var plus = '<span class="glyphicon glyphicon-plus" aria-hidden="true"></span>&nbsp;';
      newtext = plus + newtext;
      s.html(newtext);
      p.append(s).append('&nbsp;').append(c);
      d.append(p);
      $('.idea').append(d);
    });
  });
}

$(document).ready( function() {
  console.log('test');

  // $('.writing').hide();
  $('.about').hide();

  // input metaphor functionality
  $('.inputmet').click( function() {
    var w1 = $('.poetic').val();
    var w2 = $('.concrete').val();
    $('.poetic').val('');
    $('.concrete').val('');
    create_metaphor(w1, w2);
    $('.idea').empty();
    get_ideas();
  });

  // input concept functionality on enter
  $('.poetic').keypress(function (e) {
    if (e.which == 13) {
      $('.writing').show();
      $('.helper-text').hide();
      $('.about').hide();
      var w1 = $('.poetic').val();
      var w2;
      if (!metaphor.hasOwnProperty('c')) {
        w2 = concrete[Math.floor(Math.random()*concrete.length)];
      } else {
        w2 = metaphor.c;
      }
      create_metaphor(w1, w2);
      $('.idea').empty();
      get_ideas();
    }
  });

  // generating metaphor functionality
  $('.metme').click( function() {
    $('.writing').show();
    var w1 = poetic[Math.floor(Math.random()*poetic.length)];
    var w2 = concrete[Math.floor(Math.random()*concrete.length)];
    create_metaphor(w1, w2);
    $('.idea').empty();
    get_ideas();
  });

  // about button
  $('.show-about').click( function() {
    $('.about').toggle();
    $("html, body").animate({ scrollTop: $(document).height() }, "slow");
  });

  // saving metaphor functionality
  $('.save').click( function() {
    var text = $('.my-textarea').text();
    console.log('saving text:', text);
    var d = $("<div>").addClass('panel panel-default');
    var d2 = $("<div>").addClass('panel-body');
    var x = $("<button type='button' class='close' aria-label='Close'><span aria-hidden='true'>&times;</span></button>");
    d2.append(text).append(x);
    d.append(d2);
    $('.saved').append(d);
  });
});