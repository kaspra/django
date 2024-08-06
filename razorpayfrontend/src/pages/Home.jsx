import { useState } from "react";
import axios from "axios";
import useRazorpay from "react-razorpay";


export const Home = ()=>{

    const Razorpay = useRazorpay();
    const [amount,setAmount] = useState(0);

    // complete order
    const complete_order = (paymentID, orderID, signature)=>{

        axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/razorpay/order/complete/',
            data: {
                "payment_id": paymentID,
                "order_id": orderID,
                "signature": signature,
                "amount": amount
            }
        })
        .then((response)=>{
            console.log(response.data);
        })
        .catch((error)=>{
            console.log(error.response.data);
        })
    }

    const razorPay = (e)=>{
        e.preventDefault();
        //create order
        axios({
            method: 'post',
            url: 'http://127.0.0.1:8000/razorpay/order/create/',
            data: {
                amount: amount,
                currency: "INR"
            }
        })
        .then((response)=>{
            
            // get order id
            var order_id = response.data.data.id
            
            // handle payment
            const options = {
                key: process.env.REACT_APP_RAZORPAY_KEY_ID, 
                name: "Company Name",
                description: "Test Transaction",
                image: "https://example.com/your_logo",
                order_id: order_id, 
                handler: function (response) {
                    //complete order
                    complete_order(
                        response.razorpay_payment_id,
                        response.razorpay_order_id,
                        response.razorpay_signature
                    )
                },
                prefill: {
                    name: "Jack",
                    email: "jack@example.com",
                    contact: "9876543210",
                },
                notes: {
                    address: "Company Office Address",
                },
                theme: {
                    color: "#3399cc",
                },
            };

            const rzp1 = new Razorpay(options);
            rzp1.on("payment.failed", function (response) {
                alert(response.error.code);
                alert(response.error.description);
                alert(response.error.source);
                alert(response.error.step);
                alert(response.error.reason);
                alert(response.error.metadata.order_id);
                alert(response.error.metadata.payment_id);
            });
            rzp1.open();
            setAmount(0);
            
        })
        .catch((error)=>{
            console.log(error);
        })
    }

    return(
        <div className="container">
            <form onSubmit={razorPay} className="form_con">
                <h4>Razor Pay</h4>
                <input type="number" placeholder="Enter Amount" required value={amount} onChange={(e) => (setAmount(e.target.value))} />
                <button type="submit" className="btn">Pay now</button>
            </form>
        </div>
    )
}
