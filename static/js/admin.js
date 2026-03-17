// Example Backend Route for Admin Dashboard
router.get('/admin/dashboard', (req, res) => {
  // Query 1: Get Pending Delivery Agents
  const pendingAgentsQuery = "SELECT * FROM users WHERE role = 'DeliveryAgent' AND is_cleared = FALSE";
  
  // Query 2: Get all users for Admin overview
  const allUsersQuery = "SELECT id, name, email, role, is_cleared FROM users";

  // Executing queries (assuming 'db' is your SQL connection)
  db.query(pendingAgentsQuery, (err, pendingAgents) => {
    if(err) throw err;
    
    db.query(allUsersQuery, (err2, allUsers) => {
      if(err2) throw err2;
      
      // Render the page with data
      res.render('admin_dashboard', { 
        pendingAgents: pendingAgents, 
        allUsers: allUsers 
      });
    });
  });
});

// Route to handle approval button click
router.post('/admin/approve/:id', (req, res) => {
  const id = req.params.id;
  db.query("UPDATE users SET is_cleared = TRUE WHERE id = ?", [id], (err) => {
    if(err) throw err;
    res.redirect('/admin/dashboard');
  });
});