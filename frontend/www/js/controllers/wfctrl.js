(function(){
'use strict';

angular.module('Orchestra')
.controller('WfCtrl', ['$scope', 'workflows',
    function($scope, workflows) {

        $scope.workflows = workflows;
        console.log($scope.workflows);



    }]);


})();