(function(){
    'use strict';



    var getNodesAndLinks = function(ops){
        var nodes = [];
        var deferredLinks = [];
        var links = [];
        var opsByKey = {}, resByKey = {};

        _.each(ops, function(it){

            var opNodeName =  it.oid;
            
            var n = {name:opNodeName, op:it.name};
            nodes.push(n);

            var resultNode = {name:'result:'+opNodeName, op:'result', state:it.task_state, oid:it.oid}
            opsByKey[opNodeName] = n;
            resByKey[opNodeName] = resultNode;

            nodes.push(resultNode);                        

            links.push({source:n, target:resultNode, type:'resultlink'});


            var args = it.meta.args;
            _.each(args, function(arg){
                var k = opNodeName+"_" + arg;
                var argNode = {name:arg, key:k, op:'arg', type:'arg'}
                nodes.push(argNode);
                links.push({source:argNode, target:n, type:'arglink'});
                
                opsByKey[k] = argNode;

            })
            
            
            var partials = it.partials;
            for(var x in partials){
                var p = partials[x];
                var ss = opNodeName + "_" + x;

                if (angular.isObject(p)){
                    if(p.source){
                        console.log(ss)
                        deferredLinks.push({source:p.source, target:ss,type:'valuelink'})
                    }

                } else {
                    var valueNode = { key: opNodeName+'_value_'+p, name:"value_"+p, op:'value', value:p };
                    nodes.push(valueNode);
                    resByKey[valueNode.key] = valueNode;
                    deferredLinks.push({source:valueNode.key, target:ss,type:'valuelink'})

                }
            }
        });

        _.each(deferredLinks, function(l){
            console.log(1,l, resByKey, opsByKey)
            console.log(2, resByKey[l.source], opsByKey[l.target] )
            links.push({source:resByKey[l.source], target:opsByKey[l.target], type:l.type});
        })


        return {
            nodes : nodes,
            links : links

        }




    };














    //an example login form
    angular.module('Orchestra')
        .directive('wfDiagram', function($rootScope) {
            return {
                restrict: 'AE',
                //replace: 'true',
                scope : { metawf : "="},
                //template: '<svg></svg>',
                link: function(scope, elem, attrs) {
                    console.log("into wfDiagram", scope.metawf);


                    
                    var nodesAndLinks = getNodesAndLinks(scope.metawf.operations);
                    var nodes = nodesAndLinks.nodes;
                    var links = nodesAndLinks.links;


                    console.log("aaaar", nodesAndLinks)
                    
                    var $el = $(elem);

                    var width = $el.width(),
                        height = $el.height();

                    var force = d3.layout.force()
                        .nodes(nodes)
                        .links(links)
                        .size([width, height])
                        .linkDistance(function(l){
                            if(l.type == 'arglink'){
                                return 40;
                            }
                            if(l.type == 'resultlink'){
                                return 40;
                            }

                            if(l.type == 'valuelink'){
                                return 1;
                            }

                            return 100;
                        })
                        .charge(-400)
                        .on("tick", tick)
                        .start();

                    var svg = d3.select($(elem)[0]).append("svg")
                        .attr("width", width)
                        .attr("height", height);

                    var link;
                    var node;
                        
                    function start(){
                        link = svg.selectAll(".link")
                        .data(force.links());
                        
                        link.enter().append("line")
                        .attr("class", "link");

                        link.exit().remove();


                        node = svg.selectAll(".node")
                        .data(force.nodes());

                    
                        node
                        .enter()
                        .append("g")
                        .attr("class", "node")
                        //.on("mouseover", mouseover)
                        //.on("mouseout", mouseout)
                        .call(force.drag)

                        node.append("circle")
                        .classed("result", function(d){ return d.op=='result'})
                        .classed("success", function(d){ return d.state=='SUCCESS'})
                        .classed("value", function(d){ return d.op=='value'})
                        .classed("arg", function(d){ return d.op=='arg'})
                        .attr("id", function(d){ return d.oid })
                        .attr("r", function(d){
                            if(d.op == 'result'){
                                return 12;
                            }
                            if(d.op != 'value' && d.op != 'arg'){
                                return 22;
                            }
                            return 8;
                        });


                        node.append("text")
                            .attr("x", 12)
                            .attr("dy", ".35em")
                            .text(function(d) { return d.name; });
                    }    

                    

                    function tick() {
                        link
                          .attr("x1", function(d) { return d.source.x; })
                          .attr("y1", function(d) { return d.source.y; })
                          .attr("x2", function(d) { return d.target.x; })
                          .attr("y2", function(d) { return d.target.y; });
                        node
                          .attr("transform", function(d) { return "translate(" + d.x + "," + d.y + ")"; });
                    }

                    start();

                    $rootScope.$on('opsuccess', 
                        function(evt, data){
                            console.log('opsuccess', data);
                            $("#"+data)
                                .addClass('success');
                                start();

                        }
                    );

                    
                  
                }
            };
    });
    


})();