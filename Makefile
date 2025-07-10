# === DOCKER COMPOSE CONTROLS ===

up:
	@echo " Starting containers..."
	sudo docker-compose up --build -d

down:
	@echo " Stopping containers..."
	sudo docker-compose down

logs:
	@echo " Tailing logs (Ctrl+C to exit)..."
	sudo docker-compose logs -f

ps:
	@echo " Active containers:"
	sudo docker ps --filter name=Server --filter name=load_balancer

clean:
	@echo " Cleaning Docker system..."
	sudo docker system prune -f
	sudo docker volume prune -f

# === TEST RUNNER TASKS ===

a1:
	@echo " Running A1: Load Distribution Test..."
	python3 test_runner.py a1

a2:
	@echo " Running A2: Scalability Test..."
	python3 test_runner.py a2

a3:
	@echo " Running A3: Failure Recovery Test..."
	python3 test_runner.py a3

a4:
	@echo " Running A4: Hash Function Comparison..."
	python3 test_runner.py a4

report:
	@echo " Generating final report..."
	python3 test_runner.py report