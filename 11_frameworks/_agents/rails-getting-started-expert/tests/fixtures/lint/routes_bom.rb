Rails.application.routes.draw do
 root "products#index"
 resources :products do
   resources :subscribers, only: [ :create ]
 end
 resource :unsubscribe, only: [ :show ]
end
