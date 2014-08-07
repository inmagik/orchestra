(function(){
'use strict';

angular.module('Orchestra')
.controller('WfMetaCtrl', ['$scope', 'workflows',
    function($scope, workflows) {

        $scope.workflows = workflows;
        console.log($scope.workflows);



    }]);


})();