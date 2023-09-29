import React, {useEffect, useState} from 'react'
import { useDispatch, useSelector } from 'react-redux'
import { useNavigate } from 'react-router-dom';
import chart from '../assets/chart.png'
import { Link } from "react-router-dom";
import { signup } from '../actions/userActions';


const Register = () => {

	const [email, setEmail] = useState('')
	const [password, setPassword] = useState('')
	const [username, setUsername] = useState('')

	const dispatch = useDispatch()
	const navigate = useNavigate()
	const userSignup = useSelector((state) => state.userSignup)
	const { loading, error, info } = userSignup

	useEffect(() => {
		if (info) {
			console.log("userinfo in register " + info)
			navigate("/login")
		}
	}, [info])	

	const submitInfo = () => {
		console.log("signup clicked")
		dispatch(signup(username, email, password))
	} 



  return (
	<section className="h-screen">
	<div className="px-6 h-full text-gray-800">
		<div
			className="flex xl:justify-center lg:justify-between justify-center items-center flex-wrap h-full g-6"
		>
			<div
				className="grow-0 shrink-1 md:shrink-0 basis-auto xl:w-6/12 lg:w-6/12 md:w-9/12 mb-12 md:mb-0"
			>
				<img
					src={chart}
					className="w-full"
					alt="Sample image"
				/>
			</div>
			<div className="xl:ml-20 xl:w-5/12 lg:w-5/12 md:w-8/12 mb-12 md:mb-0">
				<form>
					<div className="flex flex-row items-center justify-center lg:justify-start">
						<p className="text-3xl font-bold mb-0 mr-4 -">Register</p>
					</div>

					<div className="mb-6 mt-4">
						<input
							value={username}
							onChange={(e) => setUsername(e.target.value)}
							type="text"
							className="form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
							id="exampleFormControlInput2"
							placeholder="Username"
						/>
					</div>

					<div className="mb-6 mt-4">
						<input
							value={email}
							onChange={(e) => setEmail(e.target.value)}
							type="text"
							className="form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
							id="exampleFormControlInput2"
							placeholder="Email address"
						/>
					</div>

					<div className="mb-6">
						<input
							value={password}
							onChange={(e) => setPassword(e.target.value)}
							type="password"
							className="form-control block w-full px-4 py-2 text-xl font-normal text-gray-700 bg-white bg-clip-padding border border-solid border-gray-300 rounded transition ease-in-out m-0 focus:text-gray-700 focus:bg-white focus:border-blue-600 focus:outline-none"
							id="exampleFormControlInput2"
							placeholder="Password"
						/>
					</div>

					<div className="flex justify-between items-center mb-6">
					</div>

					<div className="text-center lg:text-left">
						<button
							onClick={submitInfo}
							type="button"
							className="inline-block px-7 py-3 bg-blue-600 text-white font-medium text-sm leading-snug uppercase rounded shadow-md hover:bg-blue-700 hover:shadow-lg focus:bg-blue-700 focus:shadow-lg focus:outline-none focus:ring-0 active:bg-blue-800 active:shadow-lg transition duration-150 ease-in-out"
						>
							Register
						</button>
						<p className="text-sm font-semibold mt-2 pt-1 mb-0">
							Already have an account?
							<Link to={"/login"}
								className="text-red-600 hover:text-red-700 focus:text-red-700 transition duration-200 ease-in-out"
								>Login
							</Link>
						</p>
					</div>
				</form>
			</div>
		</div>
	</div>
</section>
  )
}

export default Register