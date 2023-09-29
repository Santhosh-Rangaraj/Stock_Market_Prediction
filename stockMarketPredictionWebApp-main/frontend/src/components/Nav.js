import React from 'react'
import { Link } from 'react-router-dom'

const Nav = () => {
	return (
		<div className="h-8 w-full bg-blue-600 flex justify-center">
			<Link to={"/"}>
				<div className="px-2 py-1 text-white">HOME</div>
			</Link> 
			<Link to={"/forecast"}>
				<div className="px-2 py-1 text-white">FORECASTING</div>
			</Link>
			<Link to={"/news-analysis"}>
				<div className="px-2 py-1 text-white">NEWS ANALYSIS</div>
			</Link>
			<Link to={"/sentiment-analysis"}>
				<div className="px-2 py-1 text-white">TWITTER ANALYSIS</div>
			</Link>
			<Link to={"/dashboard"}>
				<div className="px-2 py-1 text-white">DASHBOARD</div>
			</Link>
			<Link to={"/"}>
				<div className="px-2 py-1 text-white">LOGOUT</div>
			</Link>
		</div>
	)
}

export default Nav
