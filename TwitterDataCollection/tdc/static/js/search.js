/* global d3 */

var graph ={
   nodes:[],
   links:[]
};
var session;
function connect(){
    const host = 'bolt://localhost';
    const driver = neo4j.v1.driver(host, neo4j.v1.auth.basic("neo4j", "password"));
    session = driver.session();
    requestNodes(session);
    return session;
}

function requestNodes(session){
    const all_nodes = 'Match(n:Account) return n';
    const all_relationship = 'MATCH (a:Account)-[r:`Follow to`]->(b:Account) RETURN a.username,b.username'
    const width = 1400;
    const height = 700;
    session.run(all_nodes).then((result) => {
      // Close the neo4j session
      session.close();
      if (result.records.length > graph.nodes.length) {
          graph.nodes = [];
          for (var i in result.records) {
              var node = {};
              node.username = result.records[i]._fields[0].properties.username;
              node.name = result.records[i]._fields[0].properties.name;
              node.profile_image_url = result.records[i]._fields[0].properties.profile_image_url;
              node.tweet = result.records[i]._fields[0].properties.tweet;
              node.verified =result.records[i]._fields[0].properties.verified;
              node.time = result.records[i]._fields[0].properties.created_at;
              node.location = result.records[i]._fields[0].properties.location;
              node.followers = result.records[i]._fields[0].properties.followers.low;
              node.description = result.records[i]._fields[0].description;
              node.id_twitter = result.records[i]._fields[0].properties.id_twitter.low;
              node.url = "";
              node.x = Math.random() * width;
              node.y = Math.random() * height;
              graph.nodes.push(node);
          }
          filling();
      }
    }).catch( (error) => {
      console.error(error);
    });

    session.run(all_relationship).then((result) => {
      // Close the neo4j session
      session.close();
      if (result.records.length > graph.links.length) {
          graph.links = [];

          for (var i in result.records) {
              var link = {};
              link.source = result.records[i]._fields[0];
              link.target = result.records[i]._fields[1];
              graph.links.push(link);
          }
           filling();
      }
      // console.log('Response from Neo4j:', JSON.stringify(result, null, 2));
    }).catch( (error) => {
      console.error(error);
    });
    return true;
}
function filling(){

    var canvas = d3.select("#network"),
        width = canvas.attr("width"),
        height = canvas.attr("height"),
        ctx = canvas.node().getContext("2d"),
        r = 15,
        // color = d3.scaleOrdinal(d3.schemeCategory20),
        simulation = d3.forceSimulation()
            .force("x", d3.forceX(width/2))
            .force("y", d3.forceY(height/2))
            .force("collide", d3.forceCollide(r+1))
            .force("charge", d3.forceManyBody()
                .strength(-300))
            .on("tick",update)
            .force("link", d3.forceLink()
                .id(function (d) { return d.username;}));

    simulation.nodes(graph.nodes);
    simulation.force("link")
        .links(graph.links);

    function update() {
        requestNodes(session);
        simulation.nodes(graph.nodes);
        simulation.force("link")
            .links(graph.links);

        ctx.clearRect(0,0,width,height);
        ctx.beginPath();
    //    ctx.globalAlpha = 0.5;
        ctx.strokeStyle = "#766b70";
        graph.links.forEach(drawLink);
        ctx.stroke();


        ctx.globalAlpha = 1.0;
        graph.nodes.forEach(drawNode);


    }
    canvas
        .call(d3.drag()
            .container(canvas.node())
            .subject(dragsubject)
            .on("start", dragstarted)
            .on("drag", dragged)
            .on("end", dragended));

    function dragsubject() {
          return simulation.find(d3.event.x,d3.event.y);
     }

     function dragstarted() {
      if (!d3.event.active) simulation.alphaTarget(0.3).restart();
      d3.event.subject.fx = d3.event.subject.x;
      d3.event.subject.fy = d3.event.subject.y;
      var u = d3.event.subject;
      console.log(u);
      var username = document.getElementById("username");
      var info = document.getElementById("info");
      info.style.visibility="visible";
      fill_user(u.username,u.name,u.profile_image_url,u.tweet,
          u.verified,u.time,u.location,u.followers, u.id_twitter,u.url);


    }

    function dragged() {
      d3.event.subject.fx = d3.event.x;
      d3.event.subject.fy = d3.event.y;
    }

    function dragended() {
      if (!d3.event.active) simulation.alphaTarget(0);
      d3.event.subject.fx = null;
      d3.event.subject.fy = null;
    }

    function drawNode(d) {
      ctx.beginPath();
      ctx.fillStyle = '#FCA205';
      ctx.moveTo(d.x,d.y);
      ctx.arc(d.x,d.y,r,0,Math.PI*2);
      ctx.fill();
    }

    function drawLink(l) {
      ctx.moveTo(l.source.x,l.source.y);
      ctx.lineTo(l.target.x,l.target.y);
    }
}
function closeInfo() {
    var div = document.getElementById("info");
    div.style.visibility="hidden";


}
function fill_user(username,
                   name,
                   profile_image_url,
                   tweet,
                   verified,
                   time,
                   location,
                   followers,
                   description,
                   id_twitter,
                   url){

    var usernameA = document.getElementById("usernameP");
    var nameA = document.getElementById("nameP");
    var img = document.getElementById("imgP");
    var tweetA = document.getElementById("tweetP");
    var verifiedA = document.getElementById("verifiedP");
    var timeA = document.getElementById("timeP");
    var locationA = document.getElementById("locationP");
    var followersA = document.getElementById("followersP");
    var descriptionA = document.getElementById("description");
    var id = document.getElementById("profile_idP");
    var urlA = document.getElementById("url");
     usernameA.innerHTML = "<b>Username:</b> " + username;
     nameA.innerHTML = "<b>Name:</b> " + name;
     tweetA.innerHTML = "<b>Tweet:</b> " + tweet;
     verifiedA.innerHTML = "<b>Verified:</b> " + verified;
     timeA.innerHTML = "<b>Time:</b> " + time;
     id.innerHTML = "<b>id:</b> " + id_twitter;
     locationA.innerHTML = "<b>Location:</b> " + location;
     followersA.innerHTML = "<b>Followers:</b> " + followers + " followers.";
     descriptionA.innerHTML = "<b>Description:</b> " + description;
     img.src = profile_image_url;




}

connect()
filling();
// setInterval('filling()',1000);
//  setInterval('requestNodes(session)',2000);