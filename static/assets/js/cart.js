document.addEventListener('DOMContentLoaded', () => {
    console.log("Cart script loaded");

    let cart = JSON.parse(localStorage.getItem('cart')) || [];

    function saveCart() {
        localStorage.setItem('cart', JSON.stringify(cart));
    }

    function addToCart(id, name, image, price) {
        console.log("Adding to cart:", id, name, image, price);
        price = parseFloat(price);

        let product = cart.find(item => item.id === id);
        if (product) {
            product.quantity += 1;
        } else {
            cart.push({ id, name, image, price, quantity: 1 });
        }

        saveCart();
        updateCart();
    }

    function updateCart() {
        let cartContainer = document.querySelector('.cart-items');
        let totalContainer = document.querySelector('.cart-total');
        let cartCount = document.querySelector('.cart-count');
        
        cartContainer.innerHTML = '';

        let total = 0;
        let totalItems = 0;

        cart.forEach(product => {
            total += product.price * product.quantity;
            totalItems += product.quantity;

            let item = document.createElement('li');
            item.classList.add('list-group-item');
            item.innerHTML = `
                <div class="d-flex justify-content-between align-items-center">
                    <div>
                        <img src="${product.image}" width="40" height="40" class="me-2">
                        ${product.name} (₹${product.price.toFixed(2)})
                    </div>
                    <div>
                        <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${product.id}, ${product.quantity - 1})">-</button>
                        ${product.quantity}
                        <button class="btn btn-sm btn-outline-secondary" onclick="updateQuantity(${product.id}, ${product.quantity + 1})">+</button>
                        <button class="btn btn-sm btn-danger" onclick="removeFromCart(${product.id})">🗑</button>
                    </div>
                </div>
            `;
            cartContainer.appendChild(item);
        });

        totalContainer.innerText = total.toFixed(2);
        cartCount.innerText = totalItems;
    }

    function updateQuantity(id, newQuantity) {
        let product = cart.find(item => item.id === id);
        if (product) {
            if (newQuantity <= 0) {
                removeFromCart(id);
            } else {
                product.quantity = newQuantity;
            }
        }
        saveCart();
        updateCart();
    }

    function removeFromCart(id) {
        cart = cart.filter(item => item.id !== id);
        saveCart();
        updateCart();
    }

    function clearCart() {
        cart = [];
        saveCart();
        updateCart();
    }

    // Expose functions globally
    window.addToCart = addToCart;
    window.updateQuantity = updateQuantity;
    window.removeFromCart = removeFromCart;
    window.clearCart = clearCart;

    updateCart();
});
