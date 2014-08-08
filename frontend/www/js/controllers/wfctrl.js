(function(){
'use strict';

angular.module('Orchestra')
.controller('WfCtrl', ['$scope', 'workflows',
    function($scope, workflows) {

        $scope.workflows = workflows;
        


    }])

.controller('WfCtrlSingle', ['$scope', 'workflow',
    function($scope, workflow) {

        $scope.workflow = workflow;
        


    }]);


})();