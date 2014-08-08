(function(){
'use strict';

angular.module('Orchestra')
.controller('WfMetaCtrl', ['$scope', 'workflows',
    function($scope, workflows) {

        $scope.workflows = workflows;
        


    }])

.controller('WfMetaCtrlSingle', ['$scope', 'workflow', 'orchestraServer', '$state',
    function($scope, workflow, orchestraServer, $state) {

        $scope.workflow = workflow;

        $scope.createWorkflow = function(){
            orchestraServer.createWorkflow($scope.workflow.name)
            .then(function(resp){
                $state.go('workflows.detail', {id:resp.data.oid});
            })
        };
        



    }]);


})();