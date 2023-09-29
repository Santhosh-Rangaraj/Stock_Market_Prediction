import React, {useEffect, useState} from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom';
import { getStockForecast } from '../actions/forecastActions';
import Loader from '../components/Loader';
import Nav from '../components/Nav';

const Forecast = () => {
	const [name, setName] = useState('')
	
	const dispatch = useDispatch()

	const stockForecast = useSelector((state) => state.stockForecast)
	const {loading, error, info} = stockForecast

	useEffect(() => {
		if (info) {
			console.log(info)
		}
	}, [info])

	const submitInfo = () => {
		console.log("search clicked")
		dispatch(getStockForecast(name))
	}

	return (
		<>
		<Nav />
		<div className="flex items-center justify-center flex-col">
			<div className="mt-32 w-3/6 flex mb-4 font-bold text-lg">
				<p className="text-lg">Forecast Analysis</p>
			</div>
			<div className="mt-4 mb-6 w-3/6 flex ">
				<input
					value={name}
					onChange={(e) => setName(e.target.value)}
					type="text"
					className="form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-blue-700 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
					id="exampleFormControlInput2"
					placeholder="Company Name"
				/>
				<button
					type="button"
					onClick={submitInfo}
					className="inline-block ml-3 px-7 py-3 bg-blue-600 text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
				>Search</button>
			</div>
		{loading ? (<Loader />) : null}
		{info ? (
			<div className="w-5/6 pt-8 ">
				<div>
					<p className="text-xl font-bold">Test Accuracy</p>
					<img src={ require(`../assets/forecasts/${info}`) } className=""/>
				</div>
				<div>
					<p className="text-xl font-bold">Forecasting</p>
					<img src={ require(`../assets/predictions/${info}`) } className=""/>
				</div>
			</div>
		) : (<p></p>)}
		</div>
		</>
	)
}

export default Forecast
