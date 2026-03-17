// checks if user has specific role
function checkRole(requiredRole) {
  return (req, res, next) => {
    // Assuming req.user is populated by your login logic
    if (req.user.role !== requiredRole && req.user.role !== 'Admin') {
      return res.status(403).send("Access Denied: You do not have permission.");
    }
    next();
  };
}

// Special check for Delivery Agent Clearance
function checkAgentClearance(req, res, next) {
  if (req.user.role === 'DeliveryAgent' && !req.user.is_cleared) {
    return res.status(403).send("Access Denied: Your account is pending Admin clearance.");
  }
  next();
}

module.exports = { checkRole, checkAgentClearance };