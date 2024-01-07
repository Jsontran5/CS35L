(defun gps-line ()
  "Print the current line number and total number of lines in the buffer."
  (interactive)
  (let ((start (point-min))
        (n (line-number-at-pos))
        (newline-count 0))
    (save-excursion
      (goto-char (point-min))
      (while (search-forward "\n" nil t)
        (setq newline-count (1+ newline-count)))
      (message "Line %d/%d" n newline-count ))))
