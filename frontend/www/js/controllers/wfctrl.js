(function(){
'use strict';

angular.module('Orchestra')
.controller('WfCtrl', ['$scope', 'workflows', 'orchestraServer', '$timeout',
    function($scope, workflows, orchestraServer,$timeout) {

        $scope.workflowsData = workflows;

        $scope.$watch('workflowsData', 

            function(nv){
                console.log("cc", nv)
                if(!angular.isObject(nv)){return}
                $timeout(function(){
                    $scope.workflows = nv.results;
                });
            },  
            true
        );

        function getParameterByName(name) {
            name = name.replace(/[\[]/, "\\[").replace(/[\]]/, "\\]");
            var regex = new RegExp("[\\?&]" + name + "=([^&#]*)"),
            results = regex.exec(location.search);
            return results == null ? "" : decodeURIComponent(results[1].replace(/\+/g, " "));
        }



        $scope.loadPage = function(url){
            if(!url){return}
            orchestraServer.simpleGet(url, false).then(function(resp){
                $timeout(function(){
                    console.log("rs", resp)
                    $scope.workflowsData = resp;
                });
            })

        }
        


    }])

.controller('WfCtrlSingle', ['$rootScope', '$scope', 'workflow', 'orchestraServer', '$timeout', '$interval',
    function($rootScope, $scope, workflow, orchestraServer, $timeout, $interval) {

        $scope.workflow = workflow;
        console.log("xxx", workflow)

        $scope.runOperation = function(id){
            console.log("running operation!", id);
            orchestraServer.runOperation(id).then(function(resp){
                console.log("operation run!", resp);
            })
        };

        $scope.isPending = function(oid){
            return ($scope.workflow.pending_operations.indexOf(oid) != -1)
        }
        /*
        $scope.resetOperation = function(id){
            console.log("running operation!", id);
            orchestraServer.runOperation(id).then(function(resp){
                console.log("operation run!", resp);
            })
        }
        */

        $scope.refresh = function(){
            orchestraServer.getWorkflow($scope.workflow.oid)
            .then(function(data){
                $timeout(function(){
                    $scope.workflow = data;    
                })
                
            })
        }

        var interval = $interval($scope.refresh, 3000);

        $scope.$on("$destroy", function() {
            if (interval) {
                $interval.cancel(interval);
            }
        });

        $scope.$watch('workflow.operations', function(nv,ov){
            var oo = {}, on = {}

            _.each(nv, function(item){
                on[item.oid] = item.task_state;
            })
            _.each(ov, function(item){
                oo[item.oid] = item.task_state;
            })
            console.log("xxx", nv.operat, oo, on)
            for(var x in on){
                if(oo[x] != on[x]){
                    if(on[x] == 'SUCCESS'){
                        $rootScope.$broadcast('opsuccess', x);    
                    }
                    
                }
            }


        }, true);
        


    }]);


})();