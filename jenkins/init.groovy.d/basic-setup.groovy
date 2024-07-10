import jenkins.model.*
import hudson.security.*
import java.util.logging.Logger

def logger = Logger.getLogger("")
def instance = Jenkins.getInstance()

// Set number of executors
try {
    instance.setNumExecutors(2)
    logger.info("Set number of executors to 2")
} catch (Exception e) {
    logger.severe("Failed to set number of executors: " + e.message)
}

// Set security realm
try {
    def hudsonRealm = new HudsonPrivateSecurityRealm(false)
    def adminUsername = System.getenv('JENKINS_ADMIN_USERNAME') ?: 'admin'
    def adminPassword = System.getenv('JENKINS_ADMIN_PASSWORD') ?: 'admin'
    hudsonRealm.createAccount(adminUsername, adminPassword)
    instance.setSecurityRealm(hudsonRealm)
    logger.info("Security realm set with admin user")
} catch (Exception e) {
    logger.severe("Failed to set security realm: " + e.message)
}

// Set authorization strategy
try {
    def strategy = new FullControlOnceLoggedInAuthorizationStrategy()
    strategy.setAllowAnonymousRead(false)
    instance.setAuthorizationStrategy(strategy)
    logger.info("Authorization strategy set to FullControlOnceLoggedIn")
} catch (Exception e) {
    logger.severe("Failed to set authorization strategy: " + e.message)
}

// Enable CSRF protection (recommended)
try {
    instance.setCrumbIssuer(new hudson.security.csrf.DefaultCrumbIssuer(true))
    logger.info("CSRF Protection enabled")
} catch (Exception e) {
    logger.severe("Failed to enable CSRF Protection: " + e.message)
}

// Save the configuration
try {
    instance.save()
    logger.info("Jenkins configuration saved")
} catch (Exception e) {
    logger.severe("Failed to save Jenkins configuration: " + e.message)
}
