import jenkins.model.*
import hudson.security.*

def instance = Jenkins.getInstance()

// Set number of executors
instance.setNumExecutors(2)

// Set security realm
def hudsonRealm = new HudsonPrivateSecurityRealm(false)
hudsonRealm.createAccount('admin', 'admin')
instance.setSecurityRealm(hudsonRealm)

// Set authorization strategy
def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
strategy.setAllowAnonymousRead(false)
instance.setAuthorizationStrategy(strategy)

// Save the configuration
instance.save()
