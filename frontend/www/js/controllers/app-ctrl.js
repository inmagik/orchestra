(function(){
'use strict';

angular.module('Orchestra')
.controller('AppCtrl', ['$scope', '$http',  'DrfAuthService', 'AUTH_EVENTS', '$timeout',
    function($scope, $http, DrfAuthService, AUTH_EVENTS, $timeout) {

        
        $scope.user = {
            username : null,
            id : null
        }

        //DrfAuthService.login({'username': 'admin', 'password': 'admin'})
        $scope.testError = function(){
            $http.get('http://localhost:8000/api/users/');
        }

        //reloading user from endpoint
        $scope.$on(AUTH_EVENTS.loginSuccess, function(){
            console.log("**", $http.defaults.headers.common);
            $http.get('http://localhost:8000/api/self/').then(function(resp){
                $timeout(function(){
                    $scope.user = resp.data;
                    console.log("user", $scope.user)
                });

            });
        })


    }]);


})();