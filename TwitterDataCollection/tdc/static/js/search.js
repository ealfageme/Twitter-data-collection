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
    const all_nodes = 'Match(n:Account) return n.username';
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
              node.username = result.records[i]._fields
              node.x = Math.random() * width;
              node.y = Math.random() * height;
              graph.nodes.push(node);
          }
      }
    }).catch( (error) => {
      console.error(error);
    });

    session.run(all_relationship).then((result) => {
      // Close the neo4j session
      session.close();
      if (result.records.length < graph.length) {
          graph.links = [];
          for (var i in result.records) {
              var link = {};
              link.source = result.records[i]._fields[0];
              link.target = result.records[i]._fields[1];
              graph.links.push(link);
              //    console.log(result.records[i]._fields);
          }
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
        color = d3.scaleOrdinal(d3.schemeCategory20),
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
      console.log(d3.event.subject.username[0]);
      var username = document.getElementById("username");
      var info = document.getElementById("info");
      info.style.visibility="visible";
      username.innerHTML = d3.event.subject.username;

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


connect()
filling();
setInterval('filling()',1000);
//  setInterval('requestNodes(session)',2000);