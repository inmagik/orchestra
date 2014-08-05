(function(){

'use strict';

angular.module('drfAuth', ['http-auth-interceptor-buffer', 'LocalStorageModule'])

.constant('AUTH_EVENTS', {
    loginSuccess: 'auth-login-success',
    loginFailed: 'auth-login-failed',
    logoutSuccess: 'auth-logout-success',
    sessionTimeout: 'auth-session-timeout',
    notAuthenticated: 'auth-not-authenticated',
    notAuthorized: 'auth-not-authorized',

    // generic login required, should happen after a failed call
    // #TODO: not sure if to keep it
    loginRequired : 'auth-login-required',

})


//provider style, full blown, configurable version     
.provider('DrfConfig', function() {
    // In the provider function, you cannot inject any
    // service or factory. This can only be done at the
    // "$get" method.
 
    this.loginUrl = null;
    //mode: basic, token, ...

    this.mode = 'token'
 
    this.$get = function() {
        var url = this.url;
        return {
                loginUrl : this.loginUrl,
                mode : this.mode
            }
    };
 
    this.setLoginUrl = function(url) {
        this.loginUrl = url;
    };

    this.setMode = function(mode) {
        this.mode = mode;
    };

    
    this.write = function(){

    };

    this.read = function(){

    }

})


.service('DrfSession', ['DrfConfig', function(DrfConfig){
    this.create = function (data) {
        this.sessionData = data;
    };

    this.destroy = function(){
        this.data = null;
    };

}])


.factory('DrfAuthService', ['$rootScope',  '$http', '$q', 'AUTH_EVENTS', 'DrfSession', 'DrfConfig',
    function($rootScope, $http, $q, AUTH_EVENTS, DrfSession, DrfConfig){

        var svc = { autologin : true };
        var loginUrl = DrfConfig.loginUrl;

        var csrfToken = null;

        var loginSuccess = function(){
            if(DrfConfig.mode == 'token'){
                $http.defaults.headers.common["Authorization"] = "Token " + DrfSession.sessionData.token;
            }
            $rootScope.$broadcast(AUTH_EVENTS.loginSuccess);
        };

        var loginError = function(){
            console.log("login error detected")
            DrfSession.destroy();
            $rootScope.$broadcast(AUTH_EVENTS.loginFailed);
        };


        var logout = function(){
            if(DrfConfig.mode == 'token'){
                delete $http.defaults.headers.common["Authorization"];
                DrfSession.destroy();
                $rootScope.$broadcast(AUTH_EVENTS.logoutSuccess);

            }

        }
        

        var login = function (credentials) {
            return $http
                .post(loginUrl, credentials)
                .error(function(data){
                    loginError();
                })
                .then(function (res) {
                    DrfSession.create(res.data);
                    console.log(DrfSession)
                    loginSuccess()

                    return res;
                });
        };



        svc.login = function (credentials) {
            console.log(1 , DrfConfig)
            if(DrfConfig.mode == 'basic' && !csrfToken){
                getCrf().then(function(val){
                    credentials.csrfmiddlewaretoken = val;
                    return login(credentials)                    
                });
                
            } else {

                return login(credentials)
            }
        };

        svc.logout = logout;


        var getCrf = function(){
            var deferred = $q.defer();
            
             $http
                .get(loginUrl)
                .then(function(data){
                    var input = $(data.data).find("input[name='csrfmiddlewaretoken']");
                    if(!input.length){
                        return;
                    }
                    var token = input.val()
                    $http.defaults.headers.common["X-CSRFToken"]= token;
                    deferred.resolve(token)

                });

            return deferred.promise;
        }



        svc.isAuthenticated = function () {
            console.log(DrfSession.sessionData)
            return !!DrfSession.sessionData;
        };


        svc.loaded = true;
        if(svc.autoLogin){
          //try to login
          //...
          svc.loaded = true;


        } else {



        }



        return svc;


    }
])


.config(['$httpProvider',  function($httpProvider) {

    $httpProvider.interceptors.push(['AUTH_EVENTS', '$rootScope', '$q', 'httpBuffer', function(AUTH_EVENTS, $rootScope, $q, httpBuffer) {
      return {
        responseError: function(rejection) {

            var statuses = {
                401: AUTH_EVENTS.notAuthenticated,
                403: AUTH_EVENTS.notAuthorized,
                419: AUTH_EVENTS.sessionTimeout,
                440: AUTH_EVENTS.sessionTimeout
            };
            var msg = statuses[rejection.status] || AUTH_EVENTS.loginRequired;
            console.log("xx", msg)
            $rootScope.$broadcast(msg, rejection);
      

          if (rejection.status === 401 && !rejection.config.ignoreAuthModule) {
            var deferred = $q.defer();
            httpBuffer.append(rejection.config, deferred);
            $rootScope.$broadcast(msg, rejection);
            return deferred.promise;
          }
          // otherwise, default behaviour
          return $q.reject(rejection);
        }
      };
    }]);
}]);





/**
   * Private module, a utility, required internally by 'http-auth-interceptor'.
   */
  angular.module('http-auth-interceptor-buffer', [])

  .factory('httpBuffer', ['$injector', function($injector) {
    /** Holds all the requests, so they can be re-requested in future. */
    var buffer = [];

    /** Service initialized later because of circular dependency problem. */
    var $http;

    function retryHttpRequest(config, deferred) {
      function successCallback(response) {
        deferred.resolve(response);
      }
      function errorCallback(response) {
        deferred.reject(response);
      }
      $http = $http || $injector.get('$http');
      $http(config).then(successCallback, errorCallback);
    }

    return {
      /**
       * Appends HTTP request configuration object with deferred response attached to buffer.
       */
      append: function(config, deferred) {
        buffer.push({
          config: config,
          deferred: deferred
        });
      },

      /**
       * Abandon or reject (if reason provided) all the buffered requests.
       */
      rejectAll: function(reason) {
        if (reason) {
          for (var i = 0; i < buffer.length; ++i) {
            buffer[i].deferred.reject(reason);
          }
        }
        buffer = [];
      },

      /**
       * Retries all the buffered requests clears the buffer.
       */
      retryAll: function(updater) {
        for (var i = 0; i < buffer.length; ++i) {
          retryHttpRequest(updater(buffer[i].config), buffer[i].deferred);
        }
        buffer = [];
      }
    };
  }]);

    


}())


/*
.factory('AuthService', function ($http, Session) {
  var authService = {};
 
  authService.login = function (credentials) {
    return $http
      .post('/login', credentials)
      .then(function (res) {
        Session.create(res.id, res.user.id, res.user.role);
        return res.user;
      });
  };
 
  authService.isAuthenticated = function () {
    return !!Session.userId;
  };
 
  authService.isAuthorized = function (authorizedRoles) {
    if (!angular.isArray(authorizedRoles)) {
      authorizedRoles = [authorizedRoles];
    }
    return (authService.isAuthenticated() &&
      authorizedRoles.indexOf(Session.userRole) !== -1);
  };
 
  return authService;
})

*/