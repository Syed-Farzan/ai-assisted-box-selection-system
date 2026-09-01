# What I Learned

## 1. Understanding vague requirements into real rules

This assignment was vague about most stuff, like what dimensions do I use, can products rotate, is exact fit allowed, what if no box works, and what determines which box is better than the other if they both can keep the stuff inside. Also, can I split it with multiple boxes? I had to think about that on my own and not try to complicate stuff due to limited time, but also make sure the product was not unusable or extremely simple.

I learnt how to convert these vague requirements into real ones from this project, which is way better than normal projects since I already know most rules.

## 2.

I also learnt how to separate paths, how to use different apps and models, etc.

## 3. Database relationships

I learned database relationships, how an order is put as a foreign key in `OrderItem`, and how those order items contain a product ID and how to access one from another. I also used `prefetch_related` in a practical sense when gathering all products for weight checking, volume, etc.

## 4.

I used ORM. Though I already used that before, so...

## 5. Data validation

I learnt that too, since now I needed cost to be more than 0, and the same for weight and quantity, etc., so that was new.

## 6. Algorithm design

I learnt algorithm design, how I first get the order, then collect the order items from that order and products, and check their dimensions and compare them to boxes. If that works, then weight, and after that volume. Then I compare with every box and, in a new list, keep the usable boxes and use the best one using cost, etc.

## 7. Handling rotation

I learnt handling rotation by using sort. I compared sorted dimensions with sorted box dimensions, making it efficient without any further comparison needed.

## 8. Complex decision making

I learnt to connect multiple decisions about dimensions, weight, and volume, etc., and how that works together.

## 9. Testing

Oh, I also learnt testing, though not at a crazy good level, but I tried with what time I had.
