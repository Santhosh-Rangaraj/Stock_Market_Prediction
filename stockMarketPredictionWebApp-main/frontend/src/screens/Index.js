import React from 'react'
import { Link } from 'react-router-dom'
import finance from '../assets/finance.png'
import Nav from '../components/Nav'

const Index = () => {
	return (
		<>
			<Nav />
			<div className="w-screen h-screen">
				<div>
					<p className="text-5xl font-black pt-16 text-center">
						<u className="text-blue-700">Predict </u> and   
						<u className="text-blue-700"> Analyze</u> stock market data for free..
					</p>
				</div>
				<div className="flex">
					<img src={finance} />
					<div className="pt-48 pr-8">
						<p className="text-4xl font-bold pr-4">Analyze data from twitter and recent news and forecast the stock price using LSTM algorithm</p>
						<div className="p-5 pr-40 flex justify-end">
							<Link to={"/login"}>
								<button
									type="button"
									className="inline-block px-7 py-3 mr-4 bg-blue-600 text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
								>
									Login
								</button>
							</Link>
							<Link to={"/register"}>
								<button
									type="button"
									className="inline-block px-7 py-3 bg-blue-600 text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
								>
									Register
								</button>
							</Link>
						</div>
					</div>
				</div>
			</div>
		</>
	)
}

export default Index
