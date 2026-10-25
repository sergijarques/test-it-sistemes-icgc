import csv

def read_csv(path):
	with open(path, newline='') as csvfile:
		reader = csv.DictReader(csvfile)
		mapFile = {}
		for row in reader:
			mapFile[row['id']] = row
			row.pop('id')

		#list = list(reader)
	return mapFile


def write_csv(path, columnes, info):
	with open(path, mode='w', newline='') as csvfile:
		writer = csv.DictWriter(csvfile, fieldnames=columnes)
		writer.writeheader()

		for i in info:
			writer.writerow(i)


def tasca1(orders, products):
	order_prices = []
	for id, o in orders.items():
		preuTotal = 0;
		for p in o['products'].split(" "):
			preuTotal += float(products[p]['cost'])
		order_prices.append({'id': id, 'euros': str(preuTotal)})
	
	#print(f"{order_prices}\n\n")
	write_csv('order_prices.csv', ['id', 'euros'], order_prices)
	return order_prices


def tasca2(orders, nProducts, nCustomers):
	product_customers = {}
	for i in range(nProducts):
		product_customers[f"{i}"] = {'customer_ids': [], 'customer_added': [0]*nCustomers}

	for o in orders.values():		
		for p in o['products'].split(" "):
			customer_added = product_customers[p]['customer_added']
			customer = o['customer']
			if not customer_added[int(customer)]:
				product_customers[p]['customer_ids'].append(customer)
				customer_added[int(customer)] = 1
	
	product_customers_write = []
	for id, pc in product_customers.items():
		product_customers_write.append({'id': id, 'customer_ids': " ".join(pc['customer_ids'])})
	
	#print(f"{product_customers_write}\n\n")
	write_csv('product_customers.csv', ['id', 'customer_ids'], product_customers_write)
	return product_customers_write


def sortOrder(i):
	return float(i['total_euros'])


def tasca3(order_prices, orders, customers):
	customer_ranking = []
	customer_total_sum = {}
	for i in range(len(customers)):
		customer_total_sum[f"{i}"] = {'firstname': customers[f"{i}"]['firstname'], 'lastname': customers[f"{i}"]['lastname'], 'total_euros': 0}

	for o in order_prices:
		customer_id = orders[o['id']]['customer']
		customer_total_sum[customer_id]['total_euros'] += float(o['euros'])

	for id, cs in customer_total_sum.items():
		customer_ranking.append({'id': id, 'firstname': cs['firstname'], 'lastname': cs['lastname'], 'total_euros': str(cs['total_euros'])})
	
	customer_ranking.sort(reverse=True, key=sortOrder)
	#print(f"{customer_ranking}\n\n")

	write_csv('customer_ranking.csv', ['id', 'firstname', 'lastname', 'total_euros'], customer_ranking)
	return customer_ranking


def main():
	customers = read_csv('customers.csv')
	orders = read_csv('orders.csv')
	products = read_csv('products.csv')

	order_prices = tasca1(orders, products)
	tasca2(orders, len(products), len(customers))
	tasca3(order_prices, orders, customers)

	#print(f"customers: {customers}\n\norders: {orders}\n\nproducts: {products}")


if __name__ == "__main__":
    main()