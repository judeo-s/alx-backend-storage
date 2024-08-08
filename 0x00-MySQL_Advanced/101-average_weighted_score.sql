DELIMITER $$

CREATE PROCEDURE ComputeAverageWeightedScoreForUsers()
BEGIN
    DECLARE total_weighted_score FLOAT;
    DECLARE total_weight FLOAT;
    DECLARE user_count INT;

    SET total_weighted_score = 0;
    SET total_weight = 0;
    SET user_count = 0;

    SELECT SUM(c.score * p.weight), SUM(p.weight), COUNT(DISTINCT c.user_id)
    INTO total_weighted_score, total_weight, user_count
    FROM corrections c
    JOIN projects p ON c.project_id = p.id;

    IF user_count > 0 THEN
        SET @average_score := total_weighted_score / total_weight;
    ELSE
        SET @average_score := 0;
    END IF;

    UPDATE users
    SET average_score = @average_score;

    SELECT @average_score AS computed_average_score;
END $$

DELIMITER ;

