all: build test

build: dist/HelloWorldFunction.zip

clean:
	molecule destroy
	rm -rf dist /tmp/localstack
	docker system prune --force --volumes

dist/HelloWorldFunction.zip: sam-app/hello_world/app.py sam-app/hello_world/requirements.txt
	(cd sam-app; sam build --use-container)
	mkdir -p dist
	(cd sam-app/.aws-sam/build/HelloWorldFunction; zip -r ../../../../dist/HelloWorldFunction .)

test:
	(cd sam-app; sam local invoke HelloWorldFunction --event events/event.json)
	molecule test --destroy never
