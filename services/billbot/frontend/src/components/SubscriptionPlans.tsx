import React from 'react';
import Script from 'next/script';

declare global {
  interface Window {
    Stripe?: any;
  }
}

interface Plan {
  id: number;
  name: string;
  description: string;
  price: number;
  interval: string;
  features: string;
}

export default function SubscriptionPlans() {
  const [stripe, setStripe] = React.useState<any>(null);
  const [plans, setPlans] = React.useState<Plan[]>([]);
  const [loading, setLoading] = React.useState(true);

  React.useEffect(() => {
    if (window.Stripe) {
      setStripe(window.Stripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!));
    }
  }, []);

  React.useEffect(() => {
    fetch('/api/plans')
      .then(res => res.json())
      .then(data => {
        setPlans(data);
        setLoading(false);
      })
      .catch(err => {
        console.error('Error loading plans:', err);
        setLoading(false);
      });
  }, []);

  const handleSubscribe = async (planId: number) => {
    try {
      const response = await fetch('/api/create-checkout-session', {
        method: 'POST',
        headers: {
          'Content-Type': 'application/json',
        },
        body: JSON.stringify({
          plan_id: planId,
          success_url: `${window.location.origin}/dashboard?session_id={CHECKOUT_SESSION_ID}`,
          cancel_url: `${window.location.origin}/subscription`,
        }),
      });

      const { session_id } = await response.json();

      if (stripe) {
        const { error } = await stripe.redirectToCheckout({ sessionId: session_id });
        if (error) {
          console.error(error);
        }
      }
    } catch (error) {
      console.error('Error:', error);
    }
  };

  if (loading) {
    return <div>Loading plans...</div>;
  }

  return (
    <>
      <Script
        src="https://js.stripe.com/v3/"
        strategy="afterInteractive"
        onLoad={() => {
          if (window.Stripe) {
            setStripe(window.Stripe(process.env.NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY!));
          }
        }}
      />
      <div className="container mx-auto px-4 py-8">
        <h1 className="text-3xl font-bold text-center mb-8">Subscription Plans</h1>
        <div className="grid grid-cols-1 md:grid-cols-3 gap-8">
          {plans.map((plan) => (
            <div key={plan.id} className="border rounded-lg p-6 flex flex-col">
              <h2 className="text-xl font-semibold mb-2">{plan.name}</h2>
              <p className="text-3xl font-bold mb-4">
                ${plan.price}
                <span className="text-sm font-normal">/{plan.interval}</span>
              </p>
              <p className="text-gray-600 mb-4">{plan.description}</p>
              <ul className="mb-6 flex-grow">
                {plan.features.split('\n').map((feature, index) => (
                  <li key={index} className="flex items-center mb-2">
                    <svg className="w-4 h-4 mr-2 text-green-500" fill="currentColor" viewBox="0 0 20 20">
                      <path fillRule="evenodd" d="M16.707 5.293a1 1 0 010 1.414l-8 8a1 1 0 01-1.414 0l-4-4a1 1 0 011.414-1.414L8 12.586l7.293-7.293a1 1 0 011.414 0z" clipRule="evenodd"/>
                    </svg>
                    {feature}
                  </li>
                ))}
              </ul>
              <button
                onClick={() => handleSubscribe(plan.id)}
                className="w-full bg-blue-600 text-white py-2 px-4 rounded hover:bg-blue-700 transition-colors"
              >
                Subscribe Now
              </button>
            </div>
          ))}
        </div>
      </div>
    </>
  );
} 