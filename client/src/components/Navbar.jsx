import { Link } from "react-router"

const Navbar = () => {

  return (
    <nav>
      <h1>Welcome to your Daily Digest</h1>
      <Link to="/">Tech</Link>
      <Link to="/finance">Finance</Link>
      <Link to="/fintech">FinTech</Link>
    </nav>
  )
}

export default Navbar