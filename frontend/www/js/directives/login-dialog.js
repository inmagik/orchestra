(function(){
    'use strict';

    //an example login form
    angular.module('Orchestra')
        .directive('loginDialog', function($rootScope, DrfAuthService, AUTH_EVENTS) {
            return {
                restrict: 'AE',
                replace: 'true',
                templateUrl: 'templates/login-dialog.html',
                link: function(scope, elem, attrs) {
                    console.log("into directive login dialog");

                    var show = function(){
                        $(elem).removeClass('hide');
                    }
                    var hide = function(){
                        $(elem).addClass('hide');
                    }

                    scope.mod = { username : '', password:''};

                    scope.login = function(){
                        DrfAuthService.login(scope.mod)
                    }

                    $rootScope.$on(AUTH_EVENTS.notAuthenticated, show)
                    $rootScope.$on(AUTH_EVENTS.notAuthorized, show)
                    $rootScope.$on(AUTH_EVENTS.loginRequired, show)
                    $rootScope.$on(AUTH_EVENTS.loginSuccess, hide)
                  
                }
            };
    });
    


})();