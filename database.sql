-- MySQL Workbench Forward Engineering

SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema mydb
-- -----------------------------------------------------
-- -----------------------------------------------------
-- Schema stud_v23_ssa171
-- -----------------------------------------------------

-- -----------------------------------------------------
-- Schema stud_v23_ssa171
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `stud_v23_ssa171` DEFAULT CHARACTER SET latin1 ;
USE `stud_v23_ssa171` ;

-- -----------------------------------------------------
-- Table `stud_v23_ssa171`.`users`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stud_v23_ssa171`.`users` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `email` VARCHAR(45) NULL DEFAULT NULL,
  `first_name` VARCHAR(45) NULL DEFAULT NULL,
  `last_name` VARCHAR(45) NULL DEFAULT NULL,
  `password` VARCHAR(45) NULL DEFAULT NULL,
  `is_admin` VARCHAR(45) NULL DEFAULT '0',
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 16
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `stud_v23_ssa171`.`quiz`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stud_v23_ssa171`.`quiz` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `user_id` VARCHAR(45) NULL DEFAULT NULL,
  `title` VARCHAR(45) NULL DEFAULT NULL,
  `quiz_url` VARCHAR(45) NULL DEFAULT NULL,
  `users_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `users_id`),
  INDEX `fk_quiz_users_idx` (`users_id` ASC) VISIBLE,
  CONSTRAINT `fk_quiz_users`
    FOREIGN KEY (`users_id`)
    REFERENCES `stud_v23_ssa171`.`users` (`id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 30
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `stud_v23_ssa171`.`question`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stud_v23_ssa171`.`question` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `title` VARCHAR(255) NULL DEFAULT NULL,
  `option1` VARCHAR(100) NULL DEFAULT NULL,
  `option2` VARCHAR(100) NULL DEFAULT NULL,
  `option3` VARCHAR(100) NULL DEFAULT NULL,
  `option4` VARCHAR(100) NULL DEFAULT NULL,
  `answer` VARCHAR(45) NULL DEFAULT NULL,
  `quiz_id` INT(11) NOT NULL,
  `quiz_users_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `quiz_id`, `quiz_users_id`),
  INDEX `fk_question_quiz1_idx` (`quiz_id` ASC, `quiz_users_id` ASC) VISIBLE,
  CONSTRAINT `fk_question_quiz1`
    FOREIGN KEY (`quiz_id` , `quiz_users_id`)
    REFERENCES `stud_v23_ssa171`.`quiz` (`id` , `users_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 21
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `stud_v23_ssa171`.`answer`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stud_v23_ssa171`.`answer` (
  `id` INT(11) NOT NULL AUTO_INCREMENT,
  `question_id` VARCHAR(45) NULL DEFAULT NULL,
  `answer` VARCHAR(45) NULL DEFAULT NULL,
  `marks` VARCHAR(45) NULL DEFAULT NULL,
  `quiz_id` VARCHAR(45) NULL DEFAULT NULL,
  `user_id` VARCHAR(45) NULL DEFAULT NULL,
  `question_id1` INT(11) NOT NULL,
  `question_quiz_id` INT(11) NOT NULL,
  `question_quiz_users_id` INT(11) NOT NULL,
  PRIMARY KEY (`id`, `question_id1`, `question_quiz_id`, `question_quiz_users_id`),
  INDEX `fk_answer_question1_idx` (`question_id1` ASC, `question_quiz_id` ASC, `question_quiz_users_id` ASC) VISIBLE,
  CONSTRAINT `fk_answer_question1`
    FOREIGN KEY (`question_id1` , `question_quiz_id` , `question_quiz_users_id`)
    REFERENCES `stud_v23_ssa171`.`question` (`id` , `quiz_id` , `quiz_users_id`)
    ON DELETE NO ACTION
    ON UPDATE NO ACTION)
ENGINE = InnoDB
AUTO_INCREMENT = 33
DEFAULT CHARACTER SET = latin1;


-- -----------------------------------------------------
-- Table `stud_v23_ssa171`.`student`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `stud_v23_ssa171`.`student` (
  `id` BIGINT(20) NOT NULL AUTO_INCREMENT,
  `givenName` VARCHAR(128) NOT NULL,
  `lastName` VARCHAR(128) NOT NULL,
  `email` VARCHAR(128) NOT NULL,
  `studyProgram` VARCHAR(512) NOT NULL,
  PRIMARY KEY (`id`))
ENGINE = InnoDB
AUTO_INCREMENT = 131
DEFAULT CHARACTER SET = utf8;


SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
