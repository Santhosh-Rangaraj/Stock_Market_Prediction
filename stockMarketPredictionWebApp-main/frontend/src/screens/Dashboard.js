import axios from 'axios';
import React, {useEffect, useState} from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { getDashboard } from '../actions/dashboardAction';
import Nav from '../components/Nav';

const Dashboard = () => {
	const [data, setData] = useState([]);

	const getData = async () => {
		const token = JSON.parse(localStorage.getItem("userInfo")).access_token
		console.log(token)
		const config = {
			headers: { 
                "Authorization": `Bearer ${token}`,
                "Content-Type": "application/json"
            }
		}
		const {data} = await axios.get("http://localhost:5000/user/dashboard", config)
		console.log(data)
		setData(data)
	}
	
	useEffect(() => {
		getData()
	}, [])

	return (
		<div>
			<Nav />
			<div className="px-60">
				<p className=" py-5 font-black text-2xl">PREVIOUS FORECASTING AND PREIDCTION</p>
				{data.map(c => (
					<div>
						<p className="font-bold">{c.company}</p>
						<p className="font-bold">{c.datetime}</p>
						{c.img_url.endsWith(".png") 
							? <img src={require(`../assets/predictions/${c.img_url}`) } className="w-2/6" />	
							: <img src={require(`../assets/predictions/${c.img_url}.png`)} className="w-2/6" />
						}
					</div>
				))}
			</div>
		</div>

	)
}

export default Dashboard
