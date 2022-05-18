build:
	#lsof -t -i :8050 | xargs kill -9
	export DEBUG=False && python3 app.py &
	sleep 60
	wget -r http://127.0.0.1:8050/
	wget -r http://127.0.0.1:8050/_dash-layout
	wget -r http://127.0.0.1:8050/_dash-dependencies
	find 127.0.0.1:8050/_dash-component-suites/dash/dash-renderer/build -name "*.js" -exec sed -i 's/_dash-layout/summer_olymics_visualizations\/_dash-layout.json/g' {} \;
	find 127.0.0.1:8050/_dash-component-suites/dash/dash-renderer/build -name "*.js" -exec sed -i 's/_dash-dependencies/summer_olymics_visualizations\/_dash-dependencies.json/g' {} \;
	# Add our head
	sed -i '/<head>/ r head.html' 127.0.0.1:8050/index.html
	sed -i 's/_dash-component-suites/summer_olymics_visualizations\/_dash-component-suites/g' 127.0.0.1:8050/index.html
	sed -i 's/type="image\/x-icon" href=".*">/type="image\/x-icon" href="\/summer_olymics_visualizations\/favicon.ico">/g' 127.0.0.1:8050/index.html

	mv 127.0.0.1:8050/_dash-layout 127.0.0.1:8050/_dash-layout.json
	mv 127.0.0.1:8050/_dash-dependencies 127.0.0.1:8050/_dash-dependencies.json
	mkdir 127.0.0.1:8050/data
	cp -r ../data/* 127.0.0.1:8050/data/
	cp 127.0.0.1:8050/index.html 127.0.0.1:8050/robots.txt
	cp _static/async* 127.0.0.1:8050/_dash-component-suites/dash/dcc/
	cp _static/favicon.ico 127.0.0.1:8050/favicon.ico
	rm 127.0.0.1:8050/_favicon.ico*
	#lsof -t -i :8050 | xargs kill -9

clean:
	rm -rf 127.0.0.1:8050/