SELECT movies.movie_title, movies.movie_budget,movies.movie_revenue, credits.people_name, credits.job_name FROM `movies` 
left join credits on movies.movie_id=credits.movie_id
where credits.people_name like '%james cameron%';


SELECT count(movies.movie_title) as film_num,credits.people_name, sum( movies.movie_budget),sum(movies.movie_revenue), sum(movies.movie_revenue-movies.movie_budget) as delta FROM `movies` 
left join credits on movies.movie_id=credits.movie_id
left join productions on movies.movie_id=productions.movie_id
where credits.people_name like '%cameron%' group by credits.people_name order by delta desc ;



SELECT credits.job_name, movies.movie_title, credits.job_department,  credits.people_name, movies.movie_budget,movies.movie_revenue from movies
left join credits on movies.movie_id=credits.movie_id
where credits.people_name like '%smith%' order by movies.movie_revenue desc ;


SELECT productions.prod_name,count(movies.movie_title) totMovies, sum( movies.movie_budget),sum(movies.movie_revenue), sum(movies.movie_revenue-movies.movie_budget) as delta FROM `movies` 
left join credits on movies.movie_id=credits.movie_id
left join productions on movies.movie_id=productions.movie_id
where credits.people_name like '%smith%' group by  productions.prod_name order by delta desc limit 0,10 ;


SELECT Distinct movies.movie_original_title, credits.job_name,productions.prod_name from productions
left join credits on productions.movie_id=credits.movie_id
right join movies on movies.movie_id=productions.movie_id
where movies.movie_original_lang="en";



SELECT  movies.movie_original_title, credits.people_name as director ,productions.prod_name as producedBy from productions
left join credits on productions.movie_id=credits.movie_id
right join movies on movies.movie_id=productions.movie_id
right join languages on movies.movie_id=languages.movie_id
where languages.lang_id="it" and  credits.job_name="director";



SELECT  movies.movie_original_title, credits.people_name as director ,productions.prod_name as producedBy from productions
left join credits on productions.movie_id=credits.movie_id
right join movies on movies.movie_id=productions.movie_id
right join languages on movies.movie_id=languages.movie_id
where languages.lang_id="en" and movies.movie_original_lang="it" and credits.job_name="director";