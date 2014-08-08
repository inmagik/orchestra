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

.controller('WfCtrlSingle', ['$scope', 'workflow', 'orchestraServer',
    function($scope, workflow, orchestraServer) {

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
        


    }]);


})();