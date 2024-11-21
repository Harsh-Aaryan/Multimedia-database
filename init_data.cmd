@echo off


echo "Adding books..."
.\cli\main.py -u root -p password add ^
"book=Harry Potter;1997;JK Rowling;Bloomsbury;978-0-59-035342-7" ^
"book=Harry Potter 2;1998;JK Rowling;Bloomsbury;978-1-33-887893-6" ^
"book=Dune;1965;Frank Herbert;Chilton Book Company;978-0-44-117271-9" ^
"book=1984;1954;George Orwell;Penguin;978-1-44-343497-3" ^
"book=The Hobbit;1937;J.R.R. Tolkien;George Allen & Unwin;978-0-61-896863-3" ^
"book=The Catcher in the Rye;1951;J.D. Salinger;Little, Brown and Company;978-0-31-676948-8" ^
"book=To Kill a Mockingbird;1960;Harper Lee;J.B. Lippincott & Co.;978-0-06-112008-4" ^
"book=Brave New World;1932;Aldous Huxley;Chatto & Windus;978-0-06-085052-4" ^
"book=The Great Gatsby;1925;F. Scott Fitzgerald;Scribner;978-0-74-327356-5" ^
"book=The Fellowship of the Ring;1954;J.R.R. Tolkien;George Allen & Unwin;978-0-61-864015-7" ^
"book=The Two Towers;1954;J.R.R. Tolkien;George Allen & Unwin;978-0-61-864018-8" ^
"book=The Return of the King;1955;J.R.R. Tolkien;George Allen & Unwin;978-0-61-864020-1" ^
"book=Fahrenheit 451;1953;Ray Bradbury;Ballantine Books;978-1-45-167331-9" ^
"book=Ender's Game;1985;Orson Scott Card;Tor Books;978-0-81-255070-2" ^
"book=The Road;2006;Cormac McCarthy;Alfred A. Knopf;978-0-30-738789-9"

echo "Adding movies..."
.\cli\main.py -u root -p password add ^
"movie=The Lord of the Rings: The Fellowship of the Ring;2001;Peter Jackson;publisher;Fantasy;178" ^
"movie=Star Wars: A New Hope;1977;George Lucas;publisher;Fantasy;121" ^
"movie=The Matrix;1999;Lana Wachowski;publisher;Fantasy;136" ^
"movie=Star Wars: The Empire Strikes Back;1980;Irvin Kershner;publisher;Fantasy;124" ^
"movie=Star Trek: The Motion Picture;1979;Robert Wise;publisher;Fantasy;136" ^
"movie=Inception;2010;Christopher Nolan;publisher;Science Fiction;148" ^
"movie=Avatar;2009;James Cameron;publisher;Science Fiction;162" ^
"movie=Jurassic Park;1993;Steven Spielberg;publisher;Science Fiction;127" ^
"movie=The Dark Knight;2008;Christopher Nolan;publisher;Action;152" ^
"movie=Interstellar;2014;Christopher Nolan;publisher;Science Fiction;169" ^
"movie=Blade Runner;1982;Ridley Scott;publisher;Science Fiction;117" ^
"movie=Aliens;1986;James Cameron;publisher;Science Fiction;137" ^
"movie=The Terminator;1984;James Cameron;publisher;Science Fiction;107" ^
"movie=Mad Max: Fury Road;2015;George Miller;publisher;Action;120" ^
"movie=The Avengers;2012;Joss Whedon;publisher;Action;143"

echo "Adding music..."
.\cli\main.py -u root -p password add ^
"music=Graduation;2007;Kanye West;Graduation;Rap;226" ^
"music=A Head Full of Dreams;2015;Coldplay;A Head Full of Dreams;Pop;224" ^
"music=Bohemian Rhapsody;1975;Queen;A Night at the Opera;Rock;354" ^
"music=Hotel California;1976;Eagles;Hotel California;Rock;391" ^
"music=Shape of You;2017;Ed Sheeran;Divide;Pop;233" ^
"music=Blinding Lights;2019;The Weeknd;After Hours;Synthpop;200" ^
"music=Rolling in the Deep;2010;Adele;21;Soul;228" ^
"music=Smells Like Teen Spirit;1991;Nirvana;Nevermind;Grunge;301" ^
"music=Imagine;1971;John Lennon;Imagine;Pop Rock;183" ^
"music=Thriller;1982;Michael Jackson;Thriller;Pop;358" ^
"music=Stairway to Heaven;1971;Led Zeppelin;Led Zeppelin IV;Rock;482" ^
"music=Hey Jude;1968;The Beatles;Non-Album Single;Pop Rock;431" ^
"music=Shallow;2018;Lady Gaga & Bradley Cooper;A Star Is Born;Pop;215"

echo "Adding accounts..."
.\cli\main.py -u root -p password add ^
"account=joe345;jdog@email.com;password123" ^
"account=banana_slayer;banana@email.com;BananasAr3Th3B3st" ^
"account=jane678;jcat@email.com;password456" ^
"account=balloon_boy;ohgreatheavens@email.com;popcorn123" ^
"account=sunshine_girl;sunny@email.com;BrightDayz!" ^
"account=dragon_hunter;dragonlord@email.com;DragonSlay2024" ^
"account=pizza_lover;pizzatime@email.com;CheesePizzaRox" ^
"account=galaxy_rider;star@email.com;ToTheStars99"
